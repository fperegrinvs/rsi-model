"""Monte Carlo over anchored ranges x assumption sets x environments.

Sampling discipline (epistemic rules 1-2):
- anchored ranges (anchors.yaml) are drawn loguniformly, ONE draw per anchor per
  run, shared by every quantity referencing it — parameter-level common-cause
  correlation across sectors and delta components;
- structural coefficients stay fixed to the named assumption set; the only
  structural noise is a declared ASSUMPTION-class lognormal jitter on q
  (q_spread, reported with results);
- shock rates are jittered +-30% per run (delta.load_shocks); event fractions
  are sampled per event inside the run.

Reports P(self-expanding by T), binding-sector histogram, doubling-time
distribution, and the survival curve P(g(t) > 0) — never a single trajectory.
"""
from __future__ import annotations

from dataclasses import dataclass, replace

import numpy as np

from .delta import draw_anchors, load_anchors
from .model import Params, load_params, run


def wilson_interval(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """95% Wilson score interval for a binomial share — honest bounds even at
    k=0 or k=n (a 120/120 cell is not certainty)."""
    if n == 0:
        return (0.0, 1.0)
    ph = k / n
    denom = 1.0 + z * z / n
    center = (ph + z * z / (2 * n)) / denom
    half = z * np.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n)) / denom
    return (max(0.0, center - half), min(1.0, center + half))


@dataclass
class MCResult:
    """Frequencies across a stipulated assumption ensemble + shock process —
    NOT empirical probabilities of real-world success. Every share is reported
    with its count and Wilson interval so n is never hidden."""
    label: str
    environment: str
    n_runs: int
    horizon: float
    q_spread: float
    p_expanding: float           # share of sampled runs with g > 0 at horizon
    binding_hist: dict[str, float]   # share of ALLOCATION STEPS (pooled) binding on each sector
    doubling_times: list[float]  # first-doubling times among ALL runs that EVER doubled
    t: np.ndarray                # (T,) time grid
    survival: np.ndarray         # (T,) fraction of runs with g(t) > 0
    mean_shocks: float
    n_expanding: int = 0         # count behind p_expanding
    # survivor-conditioned: doubling times among runs ALSO expanding at horizon.
    # ever-doubled minus survivor counts = runs that doubled early, then lost
    # viability — a distinct outcome class, reported separately.
    doubling_times_survivors: list[float] = None

    @property
    def expanding_ci(self) -> tuple[float, float]:
        return wilson_interval(self.n_expanding, self.n_runs)

    def summary(self) -> str:
        d = np.array(self.doubling_times)
        dbl = (f"{np.median(d):.1f} yr (IQR {np.percentile(d, 25):.1f}-"
               f"{np.percentile(d, 75):.1f}, n={len(d)})" if len(d) else "never")
        lo, hi = self.expanding_ci
        top = sorted(self.binding_hist.items(), key=lambda kv: -kv[1])[:3]
        return (f"[{self.label}/{self.environment}] expanding @{self.horizon:g}yr: "
                f"{self.n_expanding}/{self.n_runs} = {self.p_expanding:.2f} "
                f"(95% CI {lo:.2f}-{hi:.2f}) | doubling: {dbl} | binds: "
                + ", ".join(f"{k} {v:.0%}" for k, v in top if v > 0))


def sample_params(set_name: str, env: str, rng: np.random.Generator,
                  q_spread: float = 0.10) -> Params:
    """One MC draw: anchors sampled loguniformly (shared), q jittered (ASSUMPTION)."""
    draws = draw_anchors(load_anchors(), rng)
    p = load_params(set_name, env=env, anchor_draws=draws, rng=rng)
    return replace(p, q=p.q * rng.lognormal(0.0, q_spread, p.n))


def ensemble(set_name: str = "central", env: str = "lunar", n_runs: int = 100,
             years: float = 40.0, horizon: float = 30.0, dt: float = 0.25,
             cutoff_year: float | None = None,
             cutoff_sectors: list[str] | None = None,
             shocks: bool = True, q_spread: float = 0.10,
             seed: int = 0) -> MCResult:
    rng = np.random.default_rng(seed)
    base = load_params(set_name, env=env)
    expanding, bindings, doublings, doublings_surv, n_shocks = 0, [], [], [], 0
    surv = None
    for _ in range(n_runs):
        p = sample_params(set_name, env, rng, q_spread)
        r = run(p, years=years, dt=dt, cutoff_year=cutoff_year,
                cutoff_sectors=cutoff_sectors, rng=rng if shocks else None)
        is_surv = r.self_expanding_at(horizon)
        if is_surv:
            expanding += 1
        surv = (r.g > 0).astype(float) if surv is None else surv + (r.g > 0)
        bindings.extend(r.binding.tolist())
        n_shocks += len(r.shock_log)
        d = r.doubling_time()
        if d is not None:
            doublings.append(d)
            if is_surv:
                doublings_surv.append(d)
    counts = np.bincount(np.array(bindings, int), minlength=base.n).astype(float)
    hist = dict(zip(base.sectors, (counts / counts.sum()).round(3)))
    t = np.arange(int(round(years / dt))) * dt
    return MCResult(set_name, env, n_runs, horizon, q_spread,
                    expanding / n_runs, hist, doublings,
                    t, surv / n_runs, n_shocks / n_runs, n_expanding=expanding,
                    doubling_times_survivors=doublings_surv)


@dataclass
class SensitivityResult:
    """Spearman rank correlations between each anchor's shared draw and run
    outcomes across the ensemble. Rank-based because draws are loguniform and
    outcomes non-Gaussian; anchors are drawn independently here, so plain
    per-anchor rank correlation is defensible (no Sobol assumptions needed).
    This is the displayed evidence behind any 'parameter X drives the results'
    claim — most notably the vitamin gap."""
    label: str
    environment: str
    n_runs: int
    # anchor -> (rho vs g@horizon, rho vs expansion indicator)
    rho: dict[str, tuple[float, float]]

    def ranked(self, top: int = 10) -> list[tuple[str, float, float]]:
        rows = [(a, g, e) for a, (g, e) in self.rho.items()]
        return sorted(rows, key=lambda r: -abs(r[1]))[:top]


def sensitivity(set_name: str = "central", env: str = "lunar",
                n_runs: int = 200, years: float = 32.0, horizon: float = 30.0,
                dt: float = 0.5, shocks: bool = False, q_spread: float = 0.10,
                seed: int = 0) -> SensitivityResult:
    """Global sensitivity of outcomes to anchored parameters (shocks off by
    default: isolates parameter uncertainty from event noise)."""
    from scipy.stats import spearmanr

    rng = np.random.default_rng(seed)
    anchors = load_anchors()
    draw_log, g30, expanded = [], [], []
    for _ in range(n_runs):
        draws = draw_anchors(anchors, rng)
        p = load_params(set_name, env=env, anchor_draws=draws, rng=rng)
        p = replace(p, q=p.q * rng.lognormal(0.0, q_spread, p.n))
        r = run(p, years=years, dt=dt, rng=rng if shocks else None)
        i = min(int(np.searchsorted(r.t, horizon)), len(r.g) - 1)
        draw_log.append(draws)
        g30.append(r.g[i])
        expanded.append(float(r.g[i] > 0))
    g30, expanded = np.array(g30), np.array(expanded)
    rho: dict[str, tuple[float, float]] = {}
    for name, entry in anchors.items():
        if "low" not in entry:
            continue  # point values and claims have no variation to rank
        x = np.array([d[name] for d in draw_log])
        if np.ptp(x) == 0:
            continue
        r_g = float(spearmanr(x, g30).statistic)
        r_e = (float(spearmanr(x, expanded).statistic)
               if 0 < expanded.sum() < n_runs else float("nan"))
        rho[name] = (r_g, r_e)
    return SensitivityResult(set_name, env, n_runs, rho)


def sweep_import_decay(set_name: str = "central", env: str = "lunar",
                       decay_years: np.ndarray | None = None,
                       n_runs: int = 40, years: float = 40.0,
                       horizon: float = 30.0, dt: float = 0.25,
                       shocks: bool = True, q_spread: float = 0.10,
                       seed: int = 0) -> tuple[np.ndarray, np.ndarray]:
    """P(self-expanding by horizon) vs import ramp-down e-folding time.

    The clock-setting probe as a curve: how fast can Earth supply be withdrawn
    before the system stops making it to self-expansion?
    """
    grid = np.array([4.0, 7.0, 10.0, 15.0, 25.0]) if decay_years is None else decay_years
    ps = np.empty(len(grid))
    for k, dy in enumerate(grid):
        rng = np.random.default_rng(seed + 1000 * k)
        hits = 0
        for _ in range(n_runs):
            p = replace(sample_params(set_name, env, rng, q_spread),
                        import_decay_years=float(dy))
            r = run(p, years=years, dt=dt, rng=rng if shocks else None)
            hits += r.self_expanding_at(horizon)
        ps[k] = hits / n_runs
    return grid, ps
