"""Reproducibility and metric-identity tests.

Each test targets a defect class found during external review: process-salted
seeds, uncached shared draws, unit-dependent doubling, divergent binding-sector
definitions, and committed artifacts that disagree with each other.
"""

import csv
import re
from dataclasses import replace as dc_replace
from pathlib import Path

import numpy as np
import pytest

from rsimodel import allocate_step, imports_at, load_params, run
from rsimodel.array_types import FloatArray
from rsimodel.lco import AnchorSet, lco_earth, lco_mc, lco_space
from rsimodel.model import Params
from rsimodel.montecarlo import ensemble

OUTPUTS = Path(__file__).resolve().parents[1] / "outputs"
HTML_MANUSCRIPT = (
    Path(__file__).resolve().parents[1] / "docs" / "Recursive_Industrial_Intelligence_r4.0.html"
)


# --- shared draws -----------------------------------------------------------


def test_anchorset_caches_draws() -> None:
    a = AnchorSet(np.random.default_rng(0))
    v1 = a("earth.wacc")
    v2 = a("earth.wacc")
    assert v1 == v2  # second request returns the SAME draw
    assert sum(p.quantity == "earth.wacc" for p in a.used) == 1


def test_space_and_earth_share_physical_draws_but_not_financing() -> None:
    # Common hardware properties remain correlated through one AnchorSet,
    # while the completed r4.0 boundary deliberately separates financing.
    a = AnchorSet(np.random.default_rng(42))
    lco_space("leo_inference", a=a)
    hw_after_space = a._cache["compute.hw_per_kw_it"]
    assert "space_cost_completion.wacc" in a._cache
    assert "earth.wacc" not in a._cache
    lco_earth("base", a=a)
    assert a._cache["compute.hw_per_kw_it"] == hw_after_space
    assert a._cache["space_cost_completion.wacc"] != a._cache["earth.wacc"]
    assert sum(p.quantity == "compute.hw_per_kw_it" for p in a.used) == 1
    assert sum(p.quantity == "space_cost_completion.wacc" for p in a.used) == 1
    assert sum(p.quantity == "earth.wacc" for p in a.used) == 1


def test_override_wins_even_after_cached_draw() -> None:
    a = AnchorSet(np.random.default_rng(1))
    drawn = a("earth.dc_capex_per_kw_it")
    a.overrides["earth.dc_capex_per_kw_it"] = 123.0
    assert a("earth.dc_capex_per_kw_it") == 123.0
    assert drawn != 123.0


# --- draw-stream stability under anchor-list growth -------------------------


def test_anchor_draws_stable_under_anchor_additions() -> None:
    # Adding an anchor must not change any other anchor's draw: each
    # draw is keyed by anchor NAME + run entropy, not stream position)
    from rsimodel import draw_anchors, load_anchors

    anchors = load_anchors()
    d1 = draw_anchors(anchors, np.random.default_rng(9))
    extended = dict(anchors)
    extended["zz.hypothetical_new_anchor"] = {"low": 1.0, "high": 2.0, "source_class": "ASSUMPTION"}
    d2 = draw_anchors(extended, np.random.default_rng(9))
    assert all(d1[k] == d2[k] for k in d1)
    assert "zz.hypothetical_new_anchor" in d2


def test_anchorset_draws_independent_of_request_order() -> None:
    a1 = AnchorSet(np.random.default_rng(21))
    a2 = AnchorSet(np.random.default_rng(21))
    x1, y1 = a1("earth.wacc"), a1("compute.hw_per_kw_it")
    y2, x2 = a2("compute.hw_per_kw_it"), a2("earth.wacc")
    assert x1 == x2 and y1 == y2


# --- chunk merging -----------------------------------------------------------


def test_merge_ensembles_invariants() -> None:
    from rsimodel.montecarlo import merge_ensembles

    kw = {"n_runs": 3, "years": 8, "horizon": 6, "dt": 0.5}
    parts = [ensemble("central", "lunar", seed=100 + i, **kw) for i in range(2)]
    m = merge_ensembles(parts)
    assert m.n_runs == 6
    assert m.n_expanding == sum(p.n_expanding for p in parts)
    assert m.n_sustained == sum(p.n_sustained for p in parts)
    assert len(m.lambda_horizon) == 6
    assert m.p_expanding == m.n_expanding / 6
    assert abs(sum(m.binding_hist.values()) - 1.0) < 0.02
    assert np.array_equal(m.t, parts[0].t)
    assert m.summary()


# --- deterministic seeds ----------------------------------------------------


def test_lco_mc_reproducible_across_calls() -> None:
    m1 = lco_mc("leo_inference", "base", n=50, seed=7)
    m2 = lco_mc("leo_inference", "base", n=50, seed=7)
    assert m1.ratio_pcts == m2.ratio_pcts
    assert m1.breakeven_pcts == m2.breakeven_pcts


def test_ensemble_reproducible_across_calls() -> None:
    kw = {"n_runs": 3, "years": 8, "horizon": 6, "dt": 0.5, "seed": 11}
    m1 = ensemble("central", "lunar", **kw)
    m2 = ensemble("central", "lunar", **kw)
    assert m1.n_expanding == m2.n_expanding
    assert m1.doubling_times == m2.doubling_times
    assert m1.doubling_times_balanced == m2.doubling_times_balanced
    assert m1.lambda_horizon == m2.lambda_horizon


# --- unit invariance of the replication metric ------------------------------


def test_balanced_doubling_is_unit_invariant() -> None:
    r = run(load_params("optimistic", env="lunar"), years=20)
    lam = r.lambda_series()
    # rescale one sector's arbitrary capacity unit by 10x: physical system
    # identical, λ must not move; the aggregate sum-K metric does move.
    scale = np.ones(r.K.shape[1])
    scale[2] = 10.0
    r2 = dc_replace(r, K=r.K * scale, K0=r.K0 * scale)
    assert np.allclose(r2.lambda_series(), lam)
    assert r2.balanced_doubling_time() == r.balanced_doubling_time()
    tot, tot2 = r.K.sum(axis=1)[-1], r2.K.sum(axis=1)[-1]
    assert not np.isclose(tot, tot2)  # the aggregate metric is unit-bound


def test_balanced_doubling_not_before_aggregate() -> None:
    # λ ≥ 2 requires EVERY sector doubled; sum-K doubling can be reached by
    # overbuilding easy sectors first
    r = run(load_params("optimistic", env="lunar"), years=25)
    b, d = r.balanced_doubling_time(), r.doubling_time()
    assert b is not None and d is not None
    assert b >= d - 1e-9


def test_doubling_measured_from_supplied_K0() -> None:
    p = load_params("optimistic", env="lunar")
    K0 = np.full(p.n, 2.0)
    r = run(p, K0=K0, years=5)
    assert np.allclose(r.K0, K0)  # not the post-step value
    assert r.lambda_series()[0] == pytest.approx(r.K[0].min() / 2.0, rel=1e-9)


# --- endpoint hierarchy -----------------------------------------------------


def test_sustained_implies_instantaneous() -> None:
    mc = ensemble("optimistic", "lunar", n_runs=4, years=12, horizon=10, dt=0.5, seed=3)
    assert 0 <= mc.n_sustained <= mc.n_expanding
    assert len(mc.lambda_horizon) == mc.n_runs
    assert all(value > 0 for value in mc.lambda_horizon)


# --- binding-sector definition ----------------------------------------------


def _state(p: Params, years: float = 5.0) -> tuple[FloatArray, FloatArray, FloatArray]:
    r = run(p, years=years)
    K = r.K[-1]
    m = imports_at(p, years)
    m_direct = np.where(p.stockable, 0.0, m)
    stock = r.S[-1] / 0.25
    return K, m_direct, stock


def test_binding_is_one_percent_response_argmax() -> None:
    # The binding sector is defined by a unit-invariant one-percent supply
    # relaxation, not by a raw unit-dependent dual.
    p = load_params("central", env="lunar")
    K, m_direct, stock = _state(p)
    a = allocate_step(p, K, m_direct, stock)
    g0, j = a["g"], a["binding"]
    supply = p.q * K + m_direct
    gains = np.empty(p.n)
    for i in range(p.n):
        m2 = m_direct.copy()
        m2[i] += 0.01 * max(abs(supply[i]), 1e-12)
        gains[i] = allocate_step(p, K, m2, stock)["g"] - g0
    assert gains[j] >= gains.max() - 1e-8
    assert gains[j] > 0
    assert np.allclose(gains, a["binding_responses"], atol=1e-8)
    assert a["binding_mask"][j]


def test_binding_and_actions_invariant_to_material_row_units() -> None:
    p = load_params("central", env="lunar")
    K, m_direct, stock = _state(p)
    a = allocate_step(p, K, m_direct, stock)

    # Express refining output in milli-units. Every coefficient carrying that
    # output unit changes together; the physical problem does not.
    i, scale = p.idx("refining"), 1000.0
    q = p.q.copy()
    A = p.A.copy()
    recycle_profile = p.recycle_profile.copy()
    recycle_opex = p.recycle_opex.copy()
    q[i] *= scale
    A[i] *= scale
    recycle_profile[i] *= scale
    recycle_opex[i] *= scale
    p2 = dc_replace(
        p,
        q=q,
        A=A,
        recycle_profile=recycle_profile,
        recycle_opex=recycle_opex,
    )
    m2 = m_direct.copy()
    m2[i] *= scale
    stock2 = stock.copy()
    stock2[i] *= scale
    a2 = allocate_step(p2, K, m2, stock2)
    assert a2["g"] == pytest.approx(a["g"], abs=2e-7)
    assert a2["binding"] == a["binding"]
    assert np.array_equal(a2["binding_mask"], a["binding_mask"])
    assert np.allclose(a2["binding_responses"], a["binding_responses"], atol=2e-7)
    for key in ("x", "u"):
        assert np.allclose(a2[key], a[key], atol=2e-4), key


def test_stage3_state_transition_is_history_independent() -> None:
    p = load_params("central", env="lunar")
    K, m_direct, stock = _state(p)
    a1 = allocate_step(p, K, m_direct, stock)
    # Exercise a different solver state before returning to the same problem.
    allocate_step(p, K * 1.1, m_direct, stock)
    a2 = allocate_step(p, K, m_direct, stock)
    for key in ("x", "u", "d"):
        assert np.allclose(a2[key], a1[key], atol=2e-5), key
    assert a2["w"] == pytest.approx(a1["w"], abs=2e-5)


def test_policy_binding_same_definition_as_model() -> None:
    # run_policy('myopic') and model.run must produce IDENTICAL binding
    # sequences on deterministic dynamics — one definition, both components
    from rsimodel.policies import run_policy

    p = load_params("central", env="lunar")
    r1 = run(p, years=6, dt=0.5)
    r2 = run_policy(p, policy="myopic", years=6, dt=0.5)
    assert np.array_equal(r1.binding, r2.binding)


# --- fast LP path must match the scipy reference path ------------------------


def test_fast_lp_matches_scipy() -> None:
    # the persistent-HiGHS fast path must return the same vertex, g, duals,
    # and binding as scipy.linprog on a real trajectory's states
    from rsimodel.model import _USE_FAST_LP, _allocate_scipy, _FastLP, replacement_demand

    if not _USE_FAST_LP:
        pytest.skip("fast LP unavailable or disabled")
    p = load_params("central", env="lunar")
    fast = _FastLP(p)
    n, dt = p.n, 0.5
    K = np.full(n, 1.0)
    S = np.where(p.stockable, p.stock_initial_years * replacement_demand(p, K), 0.0)
    for s_i in range(16):
        t = s_i * dt
        m = imports_at(p, t)
        m_stock = np.where(p.stockable, m, 0.0)
        m_direct = m - m_stock
        a_ref = _allocate_scipy(p, K, m_direct, S / dt)
        a_fast = fast.step(K, m_direct, S / dt)
        assert abs(a_fast["g"] - a_ref["g"]) < 1e-9
        assert a_fast["binding"] == a_ref["binding"]
        assert np.allclose(a_fast["bal_duals"], a_ref["bal_duals"], atol=1e-9)
        for k in ("x", "u", "d"):
            assert np.allclose(a_fast[k], a_ref[k], atol=2e-5), k
        K = np.maximum(K + dt * (a_ref["x"] + a_ref["u"] - p.delta * K), 1e-9)
        S = S + m_stock * dt - a_ref["d"] * dt - S * dt / p.shelf_life
        cap = p.stock_capacity_years * replacement_demand(p, K)
        S = np.clip(S, 0.0, np.where(p.stockable, np.maximum(cap, 1e-9), 0.0))


# --- committed artifacts must agree with each other -------------------------


@pytest.mark.skipif(
    not (OUTPUTS / "tables" / "mc_deep.csv").exists() or not (OUTPUTS / "report_deep.md").exists(),
    reason="deep outputs not generated",
)
def test_committed_csv_matches_committed_report() -> None:
    """Reject mc_deep.csv and report_deep.md from different runs."""
    rows = {}
    with open(OUTPUTS / "tables" / "mc_deep.csv") as f:
        for row in csv.DictReader(f):
            rows[(row["set"], row["env"])] = row
    text = (OUTPUTS / "report_deep.md").read_text()
    checked = 0
    for m in re.finditer(r"\[(\w+)/(\w+)\] expanding @(\d+)yr: (\d+)/(\d+)", text):
        set_name, env, _h, k, n = m.groups()
        assert (set_name, env) in rows, f"{set_name}/{env} missing from CSV"
        assert rows[(set_name, env)]["n_expanding"] == k, (
            f"{set_name}/{env}: report says {k}, CSV says {rows[(set_name, env)]['n_expanding']}"
        )
        assert rows[(set_name, env)]["n_runs"] == n
        checked += 1
    assert checked >= 9  # all set x env cells present


@pytest.mark.skipif(not HTML_MANUSCRIPT.exists(), reason="HTML manuscript not generated")
def test_html_manuscript_has_semantic_math_and_tables() -> None:
    """Publication regression: formulas and tables must survive conversion."""
    text = HTML_MANUSCRIPT.read_text()
    assert len(re.findall(r"<math\b", text)) >= 10
    assert len(re.findall(r"<table\b", text)) >= 10
    assert 'id="TOC"' in text
    assert '<meta name="citation_author" content="Leonardo Stern">' in text
    assert '<link rel="canonical"' not in text
    assert '<meta name="citation_public_url"' not in text
    assert 'className = "source-marker"' in text
    assert '"source-s" + match[1]' in text
    assert "$$" not in text
