"""Multisector capacity dynamics with maximin LP allocation.

Self-expansion criterion (per the paper, r2.8): feasible positive net growth in
EVERY indispensable sector, not aggregate growth. The per-step LP implements
exactly that: maximize the worst-case sector growth rate.

v1 extensions over the v0 scaffold:
- 10 sectors (repair, recycling as explicit service sectors)
- delta decomposed per environment (wear + catastrophic + obsolescence +
  logistics) from params/environments.yaml, anchored where anchors exist
- repair offsets the wear component only; recycling turns retiring capacity
  into secondary mining/refining feed
- vitamin-part stockpiles with shelf life; imports of stockable goods land in
  the stockpile (pulsed for Mars synodic resupply)
- correlated common-cause shocks (Poisson events hitting sector groups)
- per-sector import cutoffs (electronics-class cutoff scenarios)
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import yaml
from scipy.optimize import linprog

from .delta import (Provenance, Shock, assemble_delta, draw_anchors,
                    load_anchors, load_environment, load_shocks, resolve_entry)

PARAMS_DIR = Path(__file__).resolve().parents[2] / "params"


@dataclass
class Params:
    sectors: list[str]
    q: np.ndarray                 # (n,) output units per capacity unit per year (env-scaled)
    delta_comps: dict[str, np.ndarray]  # component -> (n,) fractional loss / yr
    A: np.ndarray                 # (n, n) A[i, j]: units of i's output to build 1 unit of j capacity
    import_profile: np.ndarray    # (n,) shares of import budget
    import_budget0: float
    import_decay_years: float
    # repair / recycling (service sectors)
    repair_eff: float             # capacity-units of wear offset per unit repair output
    repair_spares_fraction: float # repairing 1 unit draws this fraction of A[:, j]
    scrap_recovery: float         # fraction of retiring capacity recoverable as feed
    recycle_profile: np.ndarray   # (n,) where secondary feed lands (sums to 1)
    recycle_opex: np.ndarray      # (n,) operating inputs per unit feed produced
    # vitamin-part stockpiles
    stockable: np.ndarray         # (n,) bool
    stock_initial_years: float    # years of replacement demand pre-positioned
    stock_capacity_years: float   # max holding, years of replacement demand
    shelf_life: np.ndarray        # (n,) years (inf = indefinite)
    # environment
    shocks: list[Shock]
    pulse_years: float | None     # synodic batch period (None = continuous delivery)
    environment: str = "lunar"
    label: str = "central"
    provenance: list[Provenance] = field(default_factory=list, repr=False)

    @property
    def n(self) -> int:
        return len(self.sectors)

    @property
    def delta(self) -> np.ndarray:
        return sum(self.delta_comps.values())

    @property
    def wear(self) -> np.ndarray:
        return self.delta_comps["wear"]

    def idx(self, name: str) -> int:
        return self.sectors.index(name)


def load_params(set_name: str = "central", env: str = "lunar",
                path: Path | None = None,
                anchor_draws: dict[str, float] | None = None,
                rng: np.random.Generator | None = None) -> Params:
    """Build Params from an assumption set x environment.

    anchor_draws/rng are the Monte Carlo hooks: pass draws from
    delta.draw_anchors(anchors, rng) to sample anchored ranges; rng also
    jitters shock rates. Deterministic (geometric-mid anchors) when omitted.
    """
    from .delta import _load_yaml
    raw = _load_yaml(str(path or PARAMS_DIR / "assumptions.yaml"))
    sectors = raw["sectors"]
    s = raw["sets"][set_name]
    base = raw["sets"][s["inherit"]] if "inherit" in s else s

    env_cfg = load_environment(env)
    anchors = load_anchors()
    draws = anchor_draws if anchor_draws is not None else draw_anchors(anchors)
    comps, prov = assemble_delta(env_cfg, sectors, anchors, draws)
    scale_delta = s.get("scale_delta", 1.0)
    comps = {k: v * scale_delta for k, v in comps.items()}

    q_scale = np.empty(len(sectors))
    for i, entry in enumerate(env_cfg["q_scale"]):
        q_scale[i], pr = resolve_entry(entry, draws, anchors,
                                       f"q_scale[{sectors[i]}]")
        prov.append(pr)
    q = np.array(base["q"], float) * q_scale
    A = np.array(base["A"], float) * s.get("scale_A", 1.0)

    imp = env_cfg.get("import", {})
    profile = np.array(imp.get("profile", base["import_profile"]), float)
    budget0 = float(s.get("import_budget0", base["import_budget0"])) * float(imp.get("budget_scale", 1.0))
    decay = float(s.get("import_decay_years", base["import_decay_years"])) * float(imp.get("decay_scale", 1.0))

    rep, rec, stk = base["repair"], base["recycling"], base["stockpile"]
    stock_scale = float(s.get("scale_stock", 1.0))
    return Params(
        sectors=sectors,
        q=q,
        delta_comps=comps,
        A=A,
        import_profile=profile,
        import_budget0=budget0,
        import_decay_years=decay,
        repair_eff=float(rep["efficiency"]) * float(s.get("scale_repair_efficiency", 1.0)),
        repair_spares_fraction=float(rep["spares_fraction"]),
        scrap_recovery=min(1.0, float(rec["scrap_recovery"]) * float(s.get("scale_scrap_recovery", 1.0))),
        recycle_profile=np.array(rec["output_profile"], float),
        recycle_opex=np.array(rec["opex"], float),
        stockable=np.array(stk["stockable"], bool),
        stock_initial_years=float(stk["initial_years"]) * stock_scale,
        stock_capacity_years=float(stk["capacity_years"]) * stock_scale,
        shelf_life=np.array(stk["shelf_life_years"], float),
        shocks=load_shocks(env_cfg, sectors, rng),
        pulse_years=(float(imp["pulse_years"]) if "pulse_years" in imp else None),
        environment=env,
        label=set_name,
        provenance=prov,
    )


def imports_at(p: Params, t: float, cutoff_year: float | None = None,
               cutoff_idx: np.ndarray | None = None) -> np.ndarray:
    """Earth supply rate by sector at time t (output units / yr).

    cutoff_idx selects WHICH sectors are cut at cutoff_year (None = all):
    the electronics-class cutoff scenario is cutoff_idx=[electronics].
    """
    m = p.import_budget0 * np.exp(-t / p.import_decay_years) * p.import_profile
    if cutoff_year is not None and t >= cutoff_year:
        if cutoff_idx is None:
            m[:] = 0.0
        else:
            m[cutoff_idx] = 0.0
    return m


def replacement_demand(p: Params, K: np.ndarray) -> np.ndarray:
    """Output units of each sector needed per year just to replace retiring capacity."""
    return p.A @ (p.delta * K)


def allocate_step(p: Params, K: np.ndarray, m_direct: np.ndarray,
                  stock_avail: np.ndarray) -> dict:
    """Maximin LP over one step. Variables z = [x (n), u (n), w, d (n), g]:
      x_j  gross builds of sector j capacity
      u_j  wear offset via repair (u_j <= wear_j K_j)
      w    recycling activity (secondary feed produced / yr)
      d_i  stockpile drawdown rate (stockable i only)
      g    growth floor (maximized)

    maximize g s.t.
      x_j + u_j - delta_j K_j >= g K_j                                (growth, all j)
      A@x + sf*(A@u) + [repair row: sum(u)/eff] + [recycle row: w]
          + opex*w - recycle_profile*w - d  <=  q*K + m_direct        (material balance)
      w <= scrap_recovery * sum_j (delta_j K_j - u_j)                 (scrap cap)
      d_i <= stock_avail_i                                            (drawdown cap)

    Lexicographic second stage: with g fixed at its optimum, minimize total
    stockpile drawdown sum(d) — stock is a buffer, spent only when it actually
    buys worst-case growth, not burned greedily by the myopic step.

    Returns dict with x, u, w, d, g, binding (material-balance row with the
    smallest relative slack — the active minimum cut, scalar shadow).
    """
    n = p.n
    iw, ir = p.idx("recycling"), p.idx("repair")
    nv = 3 * n + 2
    sx, su, swv, sd, sg = 0, n, 2 * n, 2 * n + 1, 3 * n + 1

    c = np.zeros(nv)
    c[sg] = -1.0

    rows, rhs = [], []
    # growth: -x_j - u_j + g*K_j <= -delta_j*K_j
    for j in range(n):
        r = np.zeros(nv)
        r[sx + j] = -1.0
        r[su + j] = -1.0
        r[sg] = K[j]
        rows.append(r)
        rhs.append(-p.delta[j] * K[j])
    # wear cap: u_j <= wear_j*K_j
    for j in range(n):
        r = np.zeros(nv)
        r[su + j] = 1.0
        rows.append(r)
        rhs.append(p.wear[j] * K[j])
    # material balance
    supply = p.q * K + m_direct
    for i in range(n):
        r = np.zeros(nv)
        r[sx:sx + n] = p.A[i]
        r[su:su + n] = p.repair_spares_fraction * p.A[i]
        if i == ir:
            r[su:su + n] += 1.0 / p.repair_eff
        if i == iw:
            r[swv] += 1.0
        r[swv] += p.recycle_opex[i] - p.recycle_profile[i]
        r[sd + i] = -1.0
        rows.append(r)
        rhs.append(supply[i])
    # scrap cap: w + sr*sum(u) <= sr*sum(delta*K)
    r = np.zeros(nv)
    r[swv] = 1.0
    r[su:su + n] = p.scrap_recovery
    rows.append(r)
    rhs.append(p.scrap_recovery * float(np.sum(p.delta * K)))

    bounds = [(0, None)] * (3 * n + 1) + [(None, None)]
    for i in range(n):
        cap = float(stock_avail[i]) if p.stockable[i] else 0.0
        bounds[sd + i] = (0, cap)

    A_ub, b_ub = np.array(rows), np.array(rhs)
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")
    if not res.success:  # pragma: no cover — feasible with x=u=w=d=0, g <= -max(delta)
        raise RuntimeError(f"LP failed: {res.message}")
    z = res.x
    if np.any(p.stockable) and z[sd:sd + n].sum() > 1e-12:
        # stage 2: hold g at optimum (tiny tolerance), spend as little stock as possible
        g_star = z[sg]
        c2 = np.zeros(nv)
        c2[sd:sd + n] = 1.0
        pin = np.zeros(nv)
        pin[sg] = -1.0
        res2 = linprog(c2, A_ub=np.vstack([A_ub, pin]),
                       b_ub=np.append(b_ub, -(g_star - 1e-9)),
                       bounds=bounds, method="highs")
        if res2.success:
            z = res2.x
            z[sg] = g_star
    x, u, w, d, g = z[sx:sx + n], z[su:su + n], z[swv], z[sd:sd + n], z[sg]
    bal_rhs = np.array(rhs[2 * n:3 * n])
    slack = bal_rhs - np.array(rows[2 * n:3 * n]) @ z
    binding = int(np.argmin(slack / np.maximum(np.abs(bal_rhs), 1e-12)))
    return {"x": x, "u": u, "w": w, "d": d, "g": g, "binding": binding}


@dataclass
class RunResult:
    t: np.ndarray            # (T,)
    K: np.ndarray            # (T, n)
    g: np.ndarray            # (T,) maximin growth rate achieved
    binding: np.ndarray      # (T,) index of binding sector
    S: np.ndarray            # (T, n) stockpile levels (output units)
    shock_log: list[tuple[float, str, float]]  # (t, shock name, fraction lost)
    params: Params = field(repr=False, default=None)

    def self_expanding_at(self, year: float) -> bool:
        i = min(int(np.searchsorted(self.t, year)), len(self.g) - 1)
        return bool(self.g[i] > 0)

    def doubling_time(self) -> float | None:
        """Model-output replication time: years for total K to double, if it does."""
        tot = self.K.sum(axis=1)
        idx = np.argmax(tot >= 2 * tot[0])
        return float(self.t[idx]) if tot[idx] >= 2 * tot[0] else None


def run(
    p: Params,
    K0: np.ndarray | None = None,
    years: float = 40.0,
    dt: float = 0.25,
    cutoff_year: float | None = None,
    cutoff_sectors: list[str] | None = None,
    rng: np.random.Generator | None = None,
) -> RunResult:
    """Integrate the system. rng=None disables stochastic shocks (deterministic
    baseline); pass a Generator to sample common-cause events.
    cutoff_sectors names which sectors' imports stop at cutoff_year (None = all).
    """
    n = p.n
    K = np.full(n, 1.0) if K0 is None else K0.astype(float).copy()
    cutoff_idx = (None if cutoff_sectors is None
                  else np.array([p.idx(s) for s in cutoff_sectors], int))

    rep0 = replacement_demand(p, K)
    S = np.where(p.stockable, p.stock_initial_years * rep0, 0.0)

    steps = int(round(years / dt))
    T, KK, GG, BB, SS = [], [], [], [], []
    shock_log: list[tuple[float, str, float]] = []
    next_pulse = 0.0
    for s_i in range(steps):
        t = s_i * dt
        m = imports_at(p, t, cutoff_year, cutoff_idx)
        m_stock = np.where(p.stockable, m, 0.0)
        m_direct = m - m_stock
        # deliveries: continuous trickle into the stockpile, or synodic batches
        if p.pulse_years is None:
            inflow = m_stock * dt
        else:
            inflow = np.zeros(n)
            if t + dt > next_pulse - 1e-9:
                inflow = m_stock * p.pulse_years   # one synodic batch
                next_pulse += p.pulse_years

        a = allocate_step(p, K, m_direct, S / dt)
        K = np.maximum(K + dt * (a["x"] + a["u"] - p.delta * K), 1e-9)
        # stockpile: inflow - drawdown - shelf-life decay, clipped to capacity
        S = S + inflow - a["d"] * dt - S * dt / p.shelf_life
        cap = p.stock_capacity_years * replacement_demand(p, K)
        S = np.clip(S, 0.0, np.where(p.stockable, np.maximum(cap, 1e-9), 0.0))

        if rng is not None:
            for sh in p.shocks:
                for _ in range(rng.poisson(sh.rate_per_year * dt)):
                    frac = rng.uniform(*sh.fraction_lost)
                    K[sh.sector_idx] *= 1.0 - frac
                    shock_log.append((t, sh.name, frac))

        T.append(t)
        KK.append(K.copy())
        GG.append(a["g"])
        BB.append(a["binding"])
        SS.append(S.copy())
    return RunResult(np.array(T), np.array(KK), np.array(GG), np.array(BB),
                     np.array(SS), shock_log, p)
