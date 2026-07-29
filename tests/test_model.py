import numpy as np
import pytest

from rsimodel import (
    DELTA_COMPONENTS,
    allocate_step,
    imports_at,
    load_anchors,
    load_params,
    replacement_demand,
    run,
)
from rsimodel.array_types import FloatArray
from rsimodel.model import Params


def stock_at(p: Params, K: FloatArray, dt: float = 0.25) -> FloatArray:
    return np.where(p.stockable, p.stock_initial_years * replacement_demand(p, K), 0.0) / dt


def test_lp_feasible_and_material_balance() -> None:
    p = load_params("central", env="lunar")
    K = np.ones(p.n)
    m = imports_at(p, 0.0)
    m_direct = np.where(p.stockable, 0.0, m)
    a = allocate_step(p, K, m_direct, stock_at(p, K))
    assert np.all(a["x"] >= -1e-9)
    # material balance including repair spares, repair/recycling service draw, opex
    ir, iw = p.idx("repair"), p.idx("recycling")
    use = p.A @ a["x"] + p.repair_spares_fraction * (p.A @ a["u"])
    use[ir] += a["u"].sum() / p.repair_eff
    use[iw] += a["w"]
    use += p.recycle_opex * a["w"]
    supply = p.q * K + m_direct + p.recycle_profile * a["w"] + a["d"]
    assert np.all(use <= supply + 2e-5)


def test_no_imports_and_heavy_recipes_cannot_expand_everywhere() -> None:
    p = load_params("conservative", env="lunar")
    p.A[:] = p.A * 20.0
    r = run(p, years=10, cutoff_year=0.0)
    assert r.g[-1] < 0


def test_optimistic_set_self_expands() -> None:
    r = run(load_params("optimistic", env="lunar"), years=35)
    assert r.self_expanding_at(30.0)


def test_conservative_worse_than_optimistic() -> None:
    for env in ("leo", "lunar", "mars"):
        rc = run(load_params("conservative", env=env), years=20)
        ro = run(load_params("optimistic", env=env), years=20)
        assert rc.g[-1] < ro.g[-1]


def test_doubling_time_is_output_not_input() -> None:
    r = run(load_params("central", env="lunar"), years=40)
    d = r.doubling_time()
    assert d is None or d > 0.0


def test_delta_is_decomposed_with_provenance() -> None:
    p = load_params("central", env="lunar")
    total = sum(p.delta_comps[c] for c in DELTA_COMPONENTS)
    assert np.allclose(total, p.delta)
    # 4 delta components + 4 salvage factors + q_scale, each per sector
    assert len(p.provenance) == (2 * len(DELTA_COMPONENTS) + 1) * p.n
    assert any(
        pr.quantity == "q_scale[electronics]" and pr.anchor for pr in p.provenance
    )  # the vitamin gap is a sampled range
    classes = {pr.source_class for pr in p.provenance}
    assert "ASSUMPTION" in classes  # unanchored entries are declared
    assert classes & {"peer_reviewed", "technical_report", "reporting"}  # anchored ones too


def test_environments_differ_in_delta() -> None:
    d = {
        env: load_params("central", env=env).delta.sum()
        for env in ("leo", "lunar", "mars", "earth")
    }
    assert d["mars"] > d["leo"]  # logistics x2 dominates
    assert d["earth"] != d["lunar"]


def test_repair_offsets_wear_only() -> None:
    p = load_params("central", env="lunar")
    K = np.ones(p.n)
    a = allocate_step(p, K, imports_at(p, 0.0), stock_at(p, K))
    assert np.all(a["u"] <= p.wear * K + 1e-9)
    assert np.any(a["u"] > 1e-9)  # repair is actually used


def test_recycling_used_where_feed_binds() -> None:
    # LEO has no ore body (mining q_scale ~ 0): secondary feed must activate
    p = load_params("central", env="leo")
    r = run(p, years=15)
    K = r.K[-1]
    a = allocate_step(p, K, imports_at(p, 15.0), stock_at(p, K))
    assert a["w"] > 1e-6


def test_recycling_uses_only_physically_recoverable_retirement() -> None:
    from rsimodel.model import recoverable_retirement

    p = load_params("central", env="leo")
    K = np.ones(p.n)
    # LEO catastrophic and logistics losses are unavailable to recycling.
    assert np.all(p.salvage_factors["catastrophic"] == 0.0)
    assert np.all(p.salvage_factors["logistics"] == 0.0)
    expected = sum(np.sum(p.salvage_factors[c] * p.delta_comps[c] * K) for c in DELTA_COMPONENTS)
    assert recoverable_retirement(p, K) == pytest.approx(expected)
    a = allocate_step(p, K, imports_at(p, 0.0), stock_at(p, K))
    used_scrap = a["w"] + p.scrap_recovery * np.dot(p.salvage_factors["wear"], a["u"])
    assert used_scrap <= p.scrap_recovery * expected + 2e-5


def test_stockpile_bridges_electronics_cutoff() -> None:
    p = load_params("central", env="lunar")
    r = run(p, years=20, cutoff_year=5.0, cutoff_sectors=["electronics"])
    ie = p.idx("electronics")
    assert r.S[0, ie] > 0  # pre-positioned
    i_cut = int(np.searchsorted(r.t, 5.0))
    assert r.S[-1, ie] <= r.S[i_cut, ie] + 1e-9  # drained after cutoff, never refilled
    # cutoff hurts relative to open imports
    r_open = run(p, years=20)
    assert r.g[-1] <= r_open.g[-1] + 1e-9


def test_stockpile_not_burned_greedily() -> None:
    # with imports flowing, stage-2 LP keeps stock instead of draining instantly
    p = load_params("central", env="lunar")
    r = run(p, years=5)
    ie = p.idx("electronics")
    assert r.S[8, ie] > 0.2 * r.S[0, ie]  # still holding most of it at t=2
    assert not np.any(p.stockable & ~np.isfinite(p.shelf_life) & (r.S[-1] < 0))


def test_shelf_life_decays_stock() -> None:
    from dataclasses import replace

    p = load_params("central", env="lunar")
    # kill imports and give electronics a short shelf life; stock must decay
    p2 = replace(p, shelf_life=np.where(np.arange(p.n) == p.idx("electronics"), 1.0, p.shelf_life))
    r = run(p2, years=6, cutoff_year=0.0)
    ie = p.idx("electronics")
    assert r.S[-1, ie] < 0.3 * r.S[0, ie]


def test_mars_imports_arrive_in_pulses() -> None:
    p = load_params("central", env="mars")
    assert p.pulse_years is not None
    r = run(p, years=10)
    ie = p.idx("electronics")
    ds = np.diff(r.S[:, ie])
    # deliveries are lumpy: some step-to-step stock jumps far exceed the median change
    assert ds.max() > 10 * max(abs(np.median(ds)), 1e-6)


def test_shocks_reproducible_and_logged() -> None:
    p = load_params("central", env="mars")
    r1 = run(p, years=20, rng=np.random.default_rng(7))
    r2 = run(p, years=20, rng=np.random.default_rng(7))
    assert r1.shock_log == r2.shock_log
    assert len(r1.shock_log) > 0
    names = {s.name for s in p.shocks}
    assert {n for _, n, _ in r1.shock_log} <= names
    # shocks strictly hurt vs the deterministic run
    r0 = run(p, years=20)
    assert r1.K.sum(axis=1)[-1] < r0.K.sum(axis=1)[-1]


def test_growth_endpoint_is_post_shock_and_time_is_step_end() -> None:
    from dataclasses import replace

    from rsimodel import Shock

    class FixedShockRng:
        def poisson(self, _lam: float) -> int:
            return 1

        def uniform(self, lo: float, hi: float) -> float:
            return (lo + hi) / 2

    p = load_params("central", env="lunar")
    forced = Shock(
        name="forced",
        rate_per_year=1.0,
        fraction_lost=(0.5, 0.5),
        sector_idx=np.arange(p.n, dtype=int),
    )
    r = run(replace(p, shocks=[forced]), years=0.25, dt=0.25, rng=FixedShockRng())
    assert r.t.tolist() == [0.25]
    assert r.shock_log[0][0] == 0.25
    assert r.g_alloc is not None
    assert r.g_alloc[0] > 0
    assert r.g[0] < 0
    assert not r.self_expanding_at(0.25)
    assert r.allocatively_expanding_at(0.25)


def test_sector_cutoff_only_cuts_named_sectors() -> None:
    p = load_params("central", env="lunar")
    m = imports_at(p, 10.0, cutoff_year=5.0, cutoff_idx=np.array([p.idx("electronics")]))
    assert m[p.idx("electronics")] == 0.0
    assert m[p.idx("machine_tools")] > 0.0


def test_anchor_draws_stay_in_range() -> None:
    from rsimodel import draw_anchors

    anchors = load_anchors()
    rng = np.random.default_rng(0)
    for _ in range(20):
        draws = draw_anchors(anchors, rng)
        for name, v in draws.items():
            e = anchors[name]
            lo = e.get("low", e.get("value"))
            hi = e.get("high", e.get("value"))
            assert isinstance(lo, (int, float))
            assert isinstance(hi, (int, float))
            assert lo - 1e-12 <= v <= hi + 1e-12, name


def test_cut_sets_minimal_and_monotone() -> None:
    from rsimodel.cutsets import find_cut_sets

    p = load_params("central", env="lunar")
    cs = find_cut_sets(p, horizon=20, dt=1.0)
    for c in cs.minimal_cuts:
        for other in cs.minimal_cuts:
            assert c == other or not set(other) < set(c)  # no cut contains another
    assert "power" in cs.indispensable


def test_retooling_stranding_metric() -> None:
    from rsimodel.cutsets import retooling_time

    # Part IV Scenario 3: a stranded electronics tier is fatal at central
    # values (the vitamin gap makes replacement capacity a multi-decade-
    # payback asset), while power stranding under optimistic values is a
    # finite delay.
    r = retooling_time("central", "lunar", sector="electronics", dt=0.5)
    assert r.years_lost is None
    assert 0.05 < r.knocked_share < 0.20
    r2 = retooling_time("optimistic", "lunar", sector="power", dt=0.5)
    assert r2.years_lost is not None and r2.years_lost > 0


def test_mc_ensemble_smoke() -> None:
    from rsimodel.montecarlo import ensemble

    mc = ensemble("central", "lunar", n_runs=4, years=12, horizon=10, dt=0.5, seed=1)
    assert 0.0 <= mc.p_expanding <= 1.0
    assert mc.n_expanding == round(mc.p_expanding * mc.n_runs)
    lo, hi = mc.expanding_ci
    assert 0.0 <= lo <= mc.p_expanding <= hi <= 1.0
    assert len(mc.survival) == len(mc.t)
    assert mc.t[0] == 0.5 and mc.t[-1] == 12.0
    assert 0 <= mc.n_expanding <= mc.n_alloc_expanding <= mc.n_runs
    assert abs(sum(mc.binding_hist.values()) - 1.0) < 0.01
    assert mc.summary()


def test_wilson_interval_honest_at_extremes() -> None:
    from rsimodel.montecarlo import wilson_interval

    lo, hi = wilson_interval(0, 120)
    assert lo == 0.0 and 0.0 < hi < 0.05  # 0/120 is not certainty of 0
    lo, hi = wilson_interval(120, 120)
    assert 0.95 < lo < 1.0 and hi == 1.0  # 120/120 is not certainty of 1
    lo, hi = wilson_interval(0, 2000)
    assert hi < 0.003  # Part II: 0/2000 upper bound


def test_sensitivity_ranks_vitamin_gap() -> None:
    from rsimodel.montecarlo import sensitivity

    s = sensitivity("central", "lunar", n_runs=40, years=16, horizon=15, dt=1.0, seed=3)
    assert "closure.space_electronics_q_scale" in s.rho
    top = s.ranked(3)
    assert all(-1 <= rg <= 1 for _, rg, _ in top)
    # the vitamin gap must appear among the top drivers even at small n
    assert any(a == "closure.space_electronics_q_scale" for a, _, _ in top)


def test_policy_horizon_and_fallback() -> None:
    from rsimodel.policies import compare_policies, run_policy

    p = load_params("central", env="lunar")
    r_my = run_policy(p, policy="myopic", years=10, dt=1.0)
    r_hz = run_policy(p, policy="horizon", years=10, dt=1.0, horizon_steps=6)
    r_ag = run_policy(p, policy="aggregate", years=10, dt=1.0)
    for r in (r_my, r_hz, r_ag):
        assert np.all(np.isfinite(r.g)) and np.all(r.K[-1] > 0)
    # lookahead must not do materially worse than myopic on realized worst case
    assert r_hz.K[-1].sum() > 0.8 * r_my.K[-1].sum()
    pc = compare_policies(
        "central",
        "lunar",
        policies=("myopic", "horizon"),
        n_runs=2,
        years=8,
        dt=1.0,
        horizon_steps=4,
        seed=1,
    )
    assert set(pc.results) == {"myopic", "horizon"}
