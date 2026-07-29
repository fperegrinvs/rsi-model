"""Generated reports retain model boundaries, provenance, and endpoint labels."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from rsimodel.cutsets import CutProbability, CutSetResult
from rsimodel.lco import lco_earth, lco_space
from rsimodel.model import load_params, run
from rsimodel.montecarlo import MCResult
from rsimodel.report import write_part2_report, write_report


def test_part1_report_renders_all_sections(tmp_path: Path) -> None:
    params = load_params("central", env="lunar")
    result = run(params, years=1.0, dt=0.5)
    mc = MCResult(
        label="central",
        environment="lunar",
        n_runs=2,
        horizon=1.0,
        q_spread=0.1,
        p_expanding=0.5,
        binding_hist={params.sectors[0]: 1.0},
        doubling_times=[],
        t=np.array([0.5, 1.0]),
        survival=np.array([1.0, 0.5]),
        mean_shocks=0.0,
        n_expanding=1,
        lambda_horizon=[1.0, 1.1],
    )
    cut = CutSetResult(
        baseline_expanding=True,
        minimal_cuts=[("electronics",)],
        indispensable=["machine_tools"],
        horizon=1.0,
        n_sims=3,
    )
    cut_probability = CutProbability(
        label="central",
        environment="lunar",
        n_runs=2,
        horizon=1.0,
        p_baseline=0.5,
        p_fatal={("electronics",): 0.5, (): 0.0},
    )
    target = tmp_path / "report.md"
    write_report(
        {("central", "lunar"): result},
        [mc],
        {"central/lunar": cut},
        [Path("trajectory.png")],
        params,
        path=target,
        horizon=1.0,
        cut_probs=[cut_probability],
    )
    rendered = target.read_text(encoding="utf-8")
    assert "Deterministic sweeps" in rendered
    assert "Cut-set fatality over the MC ensemble" in rendered
    assert "electronics" in rendered
    assert "Parameter provenance" in rendered


def test_part2_report_renders_matched_boundaries(tmp_path: Path) -> None:
    space = lco_space("leo_inference")
    earth = lco_earth("base")
    target = tmp_path / "report_part2.md"
    write_part2_report(
        {"leo": space},
        {"base": earth},
        [],
        [Path("lco.png")],
        breakeven_notes="No probability is assigned to aspirations.",
        path=target,
    )
    rendered = target.read_text(encoding="utf-8")
    assert "Complete levelized-cost specification" in rendered
    assert "serviceable/reusable platform" in rendered
    assert "No probability is assigned to aspirations." in rendered
    assert "Parameter provenance" in rendered
