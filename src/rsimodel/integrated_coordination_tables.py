"""Generated-artifact component for the integrated pipeline."""

from __future__ import annotations

import csv

import numpy as np

from rsimodel.extensions import (
    active_graph_edge_weight,
    coordination_burden,
    coordination_burden_form,
)

from .integrated_artifacts import (
    ArtifactWorkspace,
)
from .integrated_types import IntegratedParams


def _write_coordination_extension_tables(
    workspace: ArtifactWorkspace,
    params: IntegratedParams,
) -> None:
    coordination_cfg = params.coordination_model
    with open(
        workspace.table_directory / "coordination_sensitivity.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "topology",
                "weighted_active_edges",
                "complexity_index",
                "uncertainty_index",
                "effective_intelligence_index",
                "coordination_agent_hours_per_verified_cell",
                "irreducible_floor_hours",
                "source_class",
            ]
        )
        for topology, adjacency in coordination_cfg["topology_examples"].items():
            edges = active_graph_edge_weight(np.asarray(adjacency))
            for complexity in (0.5, 1.0, 2.0):
                for uncertainty in (0.5, 1.0, 2.0):
                    for intelligence in (1.0, 2.0, 4.0):
                        burden = coordination_burden(
                            irreducible_hours=coordination_cfg["irreducible_hours"],
                            reference_hours=coordination_cfg["reference_hours"],
                            active_edge_weight=edges,
                            edge_reference=coordination_cfg["edge_reference"],
                            complexity=complexity,
                            complexity_reference=coordination_cfg["complexity_reference"],
                            uncertainty=uncertainty,
                            uncertainty_reference=coordination_cfg["uncertainty_reference"],
                            effective_intelligence=intelligence,
                            intelligence_reference=coordination_cfg["intelligence_reference"],
                            alpha=coordination_cfg["alpha"],
                            beta=coordination_cfg["beta"],
                            gamma=coordination_cfg["gamma"],
                            delta=coordination_cfg["delta"],
                            intelligence_response=coordination_cfg["intelligence_response"],
                        )
                        w.writerow(
                            [
                                topology,
                                f"{edges:.6f}",
                                f"{complexity:.6f}",
                                f"{uncertainty:.6f}",
                                f"{intelligence:.6f}",
                                f"{burden:.6f}",
                                f"{coordination_cfg['irreducible_hours']:.6f}",
                                coordination_cfg["source_class"],
                            ]
                        )

    comparison_cfg = coordination_cfg["uncertainty_comparison"]
    rng_coordination = np.random.default_rng(comparison_cfg["seed"])
    evaluation = comparison_cfg["evaluation_case"]
    evaluation_edges = active_graph_edge_weight(
        np.asarray(coordination_cfg["topology_examples"][evaluation["topology"]])
    )
    parameter_names = tuple(comparison_cfg["parameter_bounds"])
    sampled_parameters = {
        name: rng_coordination.uniform(
            float(comparison_cfg["parameter_bounds"][name][0]),
            float(comparison_cfg["parameter_bounds"][name][1]),
            int(comparison_cfg["draws"]),
        )
        for name in parameter_names
    }
    saturation_draws = rng_coordination.uniform(
        float(comparison_cfg["edge_saturation_ratio_bounds"][0]),
        float(comparison_cfg["edge_saturation_ratio_bounds"][1]),
        int(comparison_cfg["draws"]),
    )
    downstream = comparison_cfg["downstream_account"]
    coordination_uncertainty_rows = []
    for form in comparison_cfg["forms"]:
        for draw in range(int(comparison_cfg["draws"])):
            sampled = {name: float(values[draw]) for name, values in sampled_parameters.items()}
            burden = coordination_burden_form(
                form,
                irreducible_hours=sampled["irreducible_hours"],
                reference_hours=sampled["reference_hours"],
                active_edge_weight=evaluation_edges,
                edge_reference=coordination_cfg["edge_reference"],
                complexity=evaluation["complexity"],
                complexity_reference=coordination_cfg["complexity_reference"],
                uncertainty=evaluation["uncertainty"],
                uncertainty_reference=coordination_cfg["uncertainty_reference"],
                effective_intelligence=evaluation["effective_intelligence"],
                intelligence_reference=coordination_cfg["intelligence_reference"],
                alpha=sampled["alpha"],
                beta=sampled["beta"],
                gamma=sampled["gamma"],
                delta=sampled["delta"],
                intelligence_response=sampled["intelligence_response"],
                edge_saturation_ratio=float(saturation_draws[draw]),
            )
            schedule_days = burden / float(downstream["staffing_agent_hours_per_day"])
            foregone_output = schedule_days * float(downstream["verified_output_units_per_day"])
            failure_probability = min(
                float(downstream["base_failure_probability"])
                + burden
                / 100.0
                * float(downstream["failure_probability_per_100_coordination_hours"]),
                1.0,
            )
            labor_cost = burden * float(downstream["labor_cost_real_2025_usd_per_agent_hour"]) / 1e6
            coordination_uncertainty_rows.append(
                {
                    "form": form,
                    "draw": draw,
                    **sampled,
                    "edge_saturation_ratio": float(saturation_draws[draw]),
                    "burden": burden,
                    "schedule_days": schedule_days,
                    "foregone_output": foregone_output,
                    "failure_probability": failure_probability,
                    "labor_cost_musd": labor_cost,
                }
            )
    with open(
        workspace.table_directory / "coordination_form_uncertainty.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "form",
                "draw",
                *parameter_names,
                "edge_saturation_ratio",
                "weighted_active_edges",
                "complexity_index",
                "uncertainty_index",
                "effective_intelligence_index",
                "coordination_agent_hours_per_verified_cell",
                "schedule_delay_days",
                "foregone_verified_output_units",
                "failure_probability",
                "coordination_labor_cost_musd",
                "telemetry_status",
                "bound_basis",
                "accounting_rule",
                "source_class",
            ]
        )
        for row in coordination_uncertainty_rows:
            w.writerow(
                [
                    row["form"],
                    row["draw"],
                    *(f"{row[name]:.9f}" for name in parameter_names),
                    f"{row['edge_saturation_ratio']:.9f}",
                    f"{evaluation_edges:.9f}",
                    f"{evaluation['complexity']:.9f}",
                    f"{evaluation['uncertainty']:.9f}",
                    f"{evaluation['effective_intelligence']:.9f}",
                    f"{row['burden']:.9f}",
                    f"{row['schedule_days']:.9f}",
                    f"{row['foregone_output']:.9f}",
                    f"{row['failure_probability']:.9f}",
                    f"{row['labor_cost_musd']:.9f}",
                    comparison_cfg["telemetry_status"],
                    comparison_cfg["bound_basis"].strip(),
                    downstream["accounting_rule"].strip(),
                    coordination_cfg["source_class"],
                ]
            )
    with open(
        workspace.table_directory / "coordination_form_summary.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(
            [
                "form",
                "metric",
                "p10",
                "p50",
                "p90",
                "telemetry_status",
                "source_class",
            ]
        )
        metrics = (
            ("coordination_agent_hours_per_verified_cell", "burden"),
            ("schedule_delay_days", "schedule_days"),
            ("foregone_verified_output_units", "foregone_output"),
            ("failure_probability", "failure_probability"),
            ("coordination_labor_cost_musd", "labor_cost_musd"),
        )
        for form in comparison_cfg["forms"]:
            rows = [row for row in coordination_uncertainty_rows if row["form"] == form]
            for label, key in metrics:
                quantiles = np.quantile(
                    [row[key] for row in rows],
                    [0.10, 0.50, 0.90],
                )
                w.writerow(
                    [
                        form,
                        label,
                        *(f"{value:.9f}" for value in quantiles),
                        comparison_cfg["telemetry_status"],
                        coordination_cfg["source_class"],
                    ]
                )
