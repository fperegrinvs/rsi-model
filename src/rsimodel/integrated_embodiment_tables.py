"""Generated-artifact component for the integrated pipeline."""

from __future__ import annotations

import csv

import numpy as np

from rsimodel.extensions import (
    evaluate_embodiment,
)

from .integrated_artifacts import (
    ArtifactWorkspace,
)
from .integrated_types import CapacityRuns, IntegratedParams


def _write_embodiment_extension_tables(
    workspace: ArtifactWorkspace,
    params: IntegratedParams,
    runs: CapacityRuns,
) -> None:
    embodiment_bom_cfg = params.embodiment_bom
    with open(
        workspace.table_directory / "embodiment_bom_requirements.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "item",
                "producer_sector",
                "target_sector",
                "material_bom_t_per_target_capacity",
                "material_bom_total_t_per_target_capacity",
                "replacement_service_units_per_target_capacity_year",
                "replacement_recipe_coefficient",
                "source_class",
                "bounding_argument",
            ]
        )
        sector_index = {name: index for index, name in enumerate(params.sectors)}
        for item_name, item in embodiment_bom_cfg["items"].items():
            material_bom = item["material_bom_t_per_target_capacity"]
            material_text = ";".join(
                f"{element}={float(mass):g}" for element, mass in material_bom.items()
            )
            material_total = sum(float(mass) for mass in material_bom.values())
            replacement = float(item["replacement_service_units_per_target_capacity_year"])
            for target in item["target_sectors"]:
                target_index = sector_index[target]
                w.writerow(
                    [
                        item_name,
                        item["producer_sector"],
                        target,
                        material_text,
                        f"{material_total:.6f}",
                        f"{replacement:.6f}",
                        f"{replacement / params.q[target_index]:.9f}",
                        embodiment_bom_cfg["source_class"],
                        embodiment_bom_cfg["bounding_argument"].strip(),
                    ]
                )

    embodiment_cfg = params.embodiment_compatibility
    intelligence_run = runs["moon_asteroid_network"]
    verification = np.ones_like(intelligence_run.t, dtype=bool)
    with open(
        workspace.table_directory / "embodiment_compatibility_matrix.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "task",
                "sector",
                "portfolio",
                "physically_adequate",
                "failed_dimensions",
                "hardware_ceiling",
                "required_score",
                "intelligence_threshold",
                "first_passage_year",
                "failure_attribution",
                "source_class",
            ]
        )
        for task_name, task in embodiment_cfg["tasks"].items():
            for portfolio, embodiment in embodiment_cfg["portfolios"].items():
                result = evaluate_embodiment(
                    task=task_name,
                    portfolio=portfolio,
                    requirements=task["requirements"],
                    embodiment=embodiment,
                    intelligence=intelligence_run.intelligence,
                    years=intelligence_run.t,
                    verification=verification,
                    intelligence_onset=task["intelligence_onset"],
                    intelligence_scale=task["intelligence_scale"],
                    required_score=task["required_score"],
                )
                w.writerow(
                    [
                        task_name,
                        task["sector"],
                        portfolio,
                        int(result.physically_adequate),
                        ";".join(result.failed_dimensions),
                        f"{result.hardware_ceiling:.6f}",
                        f"{task['required_score']:.6f}",
                        (
                            ""
                            if result.intelligence_threshold is None
                            else f"{result.intelligence_threshold:.6f}"
                        ),
                        (
                            ""
                            if result.first_passage_year is None
                            else f"{result.first_passage_year:.6f}"
                        ),
                        result.failure_attribution,
                        embodiment_cfg["source_class"],
                    ]
                )

    sweep_cfg = embodiment_cfg["validation_sweeps"]
    sweep_portfolio = sweep_cfg["fixed_embodiment_portfolio"]
    with open(
        workspace.table_directory / "embodiment_two_direction_sweep.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "task",
                "direction",
                "sweep_value",
                "fixed_value",
                "physically_adequate",
                "hardware_ceiling",
                "verified_score",
                "required_score",
                "passes",
                "failure_attribution",
                "source_class",
            ]
        )
        for task_name, task in embodiment_cfg["tasks"].items():
            base_embodiment = embodiment_cfg["portfolios"][sweep_portfolio]
            for intelligence in sweep_cfg["intelligence_levels"]:
                result = evaluate_embodiment(
                    task=task_name,
                    portfolio=sweep_portfolio,
                    requirements=task["requirements"],
                    embodiment=base_embodiment,
                    intelligence=[intelligence],
                    years=[0.0],
                    intelligence_onset=task["intelligence_onset"],
                    intelligence_scale=task["intelligence_scale"],
                    required_score=task["required_score"],
                )
                score = float(result.score_trajectory[0])
                w.writerow(
                    [
                        task_name,
                        "vary_intelligence_hold_embodiment",
                        f"{intelligence:.6f}",
                        sweep_portfolio,
                        int(result.physically_adequate),
                        f"{result.hardware_ceiling:.6f}",
                        f"{score:.6f}",
                        f"{task['required_score']:.6f}",
                        int(score >= task["required_score"]),
                        result.failure_attribution,
                        embodiment_cfg["source_class"],
                    ]
                )
            fixed_intelligence = sweep_cfg["fixed_intelligence_level"]
            for multiplier in sweep_cfg["embodiment_quality_multipliers"]:
                varied_embodiment = {
                    dimension: min(float(value) * float(multiplier), 1.0)
                    for dimension, value in base_embodiment.items()
                }
                result = evaluate_embodiment(
                    task=task_name,
                    portfolio=f"{sweep_portfolio}_x{multiplier:g}",
                    requirements=task["requirements"],
                    embodiment=varied_embodiment,
                    intelligence=[fixed_intelligence],
                    years=[0.0],
                    intelligence_onset=task["intelligence_onset"],
                    intelligence_scale=task["intelligence_scale"],
                    required_score=task["required_score"],
                )
                score = float(result.score_trajectory[0])
                w.writerow(
                    [
                        task_name,
                        "vary_embodiment_hold_intelligence",
                        f"{multiplier:.6f}",
                        f"{fixed_intelligence:.6f}",
                        int(result.physically_adequate),
                        f"{result.hardware_ceiling:.6f}",
                        f"{score:.6f}",
                        f"{task['required_score']:.6f}",
                        int(score >= task["required_score"]),
                        result.failure_attribution,
                        embodiment_cfg["source_class"],
                    ]
                )

    fault_portfolio = embodiment_cfg["portfolios"]["hybrid"]
    fault_intelligence = sweep_cfg["fixed_intelligence_level"]
    with open(
        workspace.table_directory / "terrestrial_rehearsal_embodiment_faults.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "scenario",
                "task",
                "fault",
                "dimension_multipliers",
                "physically_adequate",
                "failed_dimensions",
                "verified_score",
                "required_score",
                "passes",
                "failure_attribution",
                "source_class",
            ]
        )
        for fault_name, multipliers in embodiment_cfg["terrestrial_rehearsal_faults"].items():
            degraded = {
                dimension: float(value) * float(multipliers.get(dimension, 1.0))
                for dimension, value in fault_portfolio.items()
            }
            for task_name, task in embodiment_cfg["tasks"].items():
                result = evaluate_embodiment(
                    task=task_name,
                    portfolio=f"hybrid_{fault_name}",
                    requirements=task["requirements"],
                    embodiment=degraded,
                    intelligence=[fault_intelligence],
                    years=[0.0],
                    intelligence_onset=task["intelligence_onset"],
                    intelligence_scale=task["intelligence_scale"],
                    required_score=task["required_score"],
                )
                score = float(result.score_trajectory[0])
                w.writerow(
                    [
                        "terrestrial_rehearsal",
                        task_name,
                        fault_name,
                        ";".join(f"{name}={value:g}" for name, value in multipliers.items()),
                        int(result.physically_adequate),
                        ";".join(result.failed_dimensions),
                        f"{score:.6f}",
                        f"{task['required_score']:.6f}",
                        int(score >= task["required_score"]),
                        result.failure_attribution,
                        embodiment_cfg["source_class"],
                    ]
                )
