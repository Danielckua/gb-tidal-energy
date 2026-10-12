"""Summarise the supplied hourly CPLEX archive without importing PyPSA.

Run from any directory. Component parameters are read from notebook syntax;
no notebook code is executed. All snapshots have a duration of one hour.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import operator
from pathlib import Path
from zipfile import ZipFile

import numpy as np
import pandas as pd

MODEL_DIR = Path(__file__).resolve().parent
SCENARIOS = ["scenario_0", "scenario_1_z1", "scenario_2_z9", "scenario_3_z15", "scenario_4_all"]
OPERATORS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul}


def constant(node):
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
        return OPERATORS[type(node.op)](constant(node.left), constant(node.right))
    raise ValueError(f"Unsupported component expression: {ast.unparse(node)}")


def components(scenario):
    notebook = json.loads((MODEL_DIR / f"{scenario}.ipynb").read_text(encoding="utf-8"))
    source = "\n".join("".join(c["source"]) for c in notebook["cells"] if c["cell_type"] == "code")
    generators, loads = {}, {}
    for node in ast.walk(ast.parse(source)):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and isinstance(node.func.value, ast.Name) and node.func.value.id == "network"
                and node.func.attr == "add" and len(node.args) >= 2):
            continue
        kind, name = map(constant, node.args[:2])
        args = {k.arg: k.value for k in node.keywords}
        if kind == "Generator":
            info = {k: constant(args[k]) for k in ("bus", "p_nom", "marginal_cost")}
            if "p_max_pu" in args:
                expression = args["p_max_pu"]
                if not (isinstance(expression, ast.Call) and ast.unparse(expression.func) == "np.array"
                        and len(expression.args) == 1 and isinstance(expression.args[0], ast.Subscript)
                        and ast.unparse(expression.args[0].value) == "timeseries_data"):
                    raise ValueError(f"Unsupported availability expression for {name}")
                info["profile"] = constant(expression.args[0].slice)
            generators[name] = info
        elif kind == "Load":
            expression = args["p_set"]
            if not (isinstance(expression, ast.BinOp) and isinstance(expression.op, ast.Mult)
                    and ast.unparse(expression.left) == "GB_load"):
                raise ValueError(f"Unsupported demand expression for {name}")
            bus = constant(args["bus"])
            loads[bus] = loads.get(bus, 0.0) + constant(expression.right)
    return generators, loads


def hourly_csv(archive, scenario, suffix):
    name = f"{scenario}/pypsa_results_{suffix}.csv"
    with archive.open(name) as stream:
        frame = pd.read_csv(stream, index_col=0)
    if not frame.index.equals(pd.Index(range(8760))) or not frame.columns.is_unique:
        raise ValueError(f"Expected 8,760 indexed hourly rows and unique columns in {name}")
    if not np.isfinite(frame.to_numpy(dtype=float)).all():
        raise ValueError(f"Non-finite values in {name}")
    return frame


def analyse(archive, scenario, inputs):
    generators, shares = components(scenario)
    dispatch = hourly_csv(archive, scenario, "gen")
    prices = hourly_csv(archive, scenario, "marginal_price")
    storage = hourly_csv(archive, scenario, "stor")
    flows = hourly_csv(archive, scenario, "network")
    if set(dispatch.columns) != set(generators) or set(prices.columns) != set(shares):
        raise ValueError(f"Archive/model component mismatch in {scenario}")
    energy = dispatch.sum()
    costs = pd.Series({name: g["marginal_cost"] for name, g in generators.items()})
    operating_cost = energy * costs
    potential = pd.Series({name: g["p_nom"] * inputs[g["profile"]].sum()
                           for name, g in generators.items() if "profile" in g})
    res_names = [n for n in dispatch if any(t in n for t in ("Solar PV", "Wind", "Tidal Stream"))]
    if set(potential.index) != set(res_names):
        raise ValueError(f"Unexpected renewable profile configuration in {scenario}")
    for name, info in generators.items():
        available = (info["p_nom"] * inputs[info["profile"]].to_numpy()
                     if "profile" in info else info["p_nom"])
        if (dispatch[name].to_numpy() > available + 0.02).any() or dispatch[name].min() < -0.02:
            raise ValueError(f"Dispatch outside available capacity: {scenario}, {name}")
    res_energy = float(energy[res_names].sum())
    tidal_names = [n for n in res_names if "Tidal Stream" in n]
    gas_names = [n for n in dispatch if n.split("-", 1)[-1].strip() in ("CCGT", "CHP", "Gas", "OCGT")]
    import_names = [n for n in dispatch if "Interconnector" in n]
    shed_names = [n for n in dispatch if "Load shed" in n]
    demand = pd.DataFrame({bus: inputs["Demand"].to_numpy() * share for bus, share in shares.items()})
    revenue = sum(float((dispatch[n] * prices[g["bus"]]).sum()) for n, g in generators.items() if n in res_names)
    row = {
        "scenario": scenario,
        "operating_cost_million_GBP": float(operating_cost.sum()) / 1e6,
        "generation_TWh": float(energy.sum()) / 1e6,
        "variable_RES_generation_TWh": res_energy / 1e6,
        "variable_RES_available_TWh": float(potential.sum()) / 1e6,
        "variable_RES_curtailment_TWh": float((potential - energy[potential.index]).sum()) / 1e6,
        "tidal_generation_TWh": float(energy[tidal_names].sum()) / 1e6,
        "tidal_available_TWh": float(potential[tidal_names].sum()) / 1e6,
        "gas_generation_TWh": float(energy[gas_names].sum()) / 1e6,
        "imports_TWh": float(energy[import_names].sum()) / 1e6,
        "load_shedding_TWh": float(energy[shed_names].sum()) / 1e6,
        "demand_TWh": float(demand.to_numpy().sum()) / 1e6,
        "average_generation_cost_GBP_per_MWh": float(operating_cost.sum() / energy.sum()),
        "RES_capture_price_GBP_per_MWh": revenue / res_energy,
        "demand_weighted_market_price_GBP_per_MWh": float((prices * demand).to_numpy().sum() / demand.to_numpy().sum()),
        "storage_net_dispatch_TWh": float(storage.to_numpy().sum()) / 1e6,
        "maximum_absolute_link_flow_MW": float(np.abs(flows.to_numpy()).max()),
    }
    zones = []
    for bus in sorted(shares, key=lambda b: int(b[1:])):
        names = [n for n, g in generators.items() if g["bus"] == bus]
        renewable_names = [n for n in names if n in res_names]
        total = float(energy[names].sum())
        res_total = float(energy[renewable_names].sum())
        zones.append({
            "scenario": scenario, "zone": bus,
            "generation_TWh": total / 1e6,
            "average_generation_cost_GBP_per_MWh": float(operating_cost[names].sum()) / total if total else np.nan,
            "RES_capture_price_GBP_per_MWh": sum(float((dispatch[n] * prices[bus]).sum()) for n in renewable_names) / res_total if res_total else np.nan,
            "demand_weighted_market_price_GBP_per_MWh": float((prices[bus] * demand[bus]).sum() / demand[bus].sum()),
        })
    return row, zones


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, default=MODEL_DIR.parent / "initial_results/GB_tidal_CPLEX_reference_results.zip")
    parser.add_argument("--output-dir", type=Path, default=MODEL_DIR / "outputs/reference_summary")
    args = parser.parse_args()
    inputs = pd.read_csv(MODEL_DIR / "Inputs_2030.csv")
    if len(inputs) != 8760 or not np.isfinite(inputs.to_numpy(dtype=float)).all():
        raise ValueError("Expected 8,760 finite hourly input rows")
    rows, zones = [], []
    with ZipFile(args.archive) as archive:
        for scenario in SCENARIOS:
            row, zonal_rows = analyse(archive, scenario, inputs)
            rows.append(row)
            zones.extend(zonal_rows)
    summary = pd.DataFrame(rows).set_index("scenario")
    for metric in ("operating_cost_million_GBP", "variable_RES_generation_TWh", "variable_RES_curtailment_TWh", "gas_generation_TWh", "tidal_available_TWh", "tidal_generation_TWh"):
        summary[f"delta_{metric}"] = summary[metric] - summary.loc["scenario_0", metric]
    added_energy = summary["delta_tidal_available_TWh"].replace(0, np.nan)
    summary["cost_delta_per_added_available_tidal_GBP_per_MWh"] = summary["delta_operating_cost_million_GBP"] / added_energy
    summary["cost_delta_per_added_dispatched_tidal_GBP_per_MWh"] = summary["delta_operating_cost_million_GBP"] / summary["delta_tidal_generation_TWh"].replace(0, np.nan)
    zonal = pd.DataFrame(zones).set_index(["scenario", "zone"])
    for metric in ("average_generation_cost_GBP_per_MWh", "RES_capture_price_GBP_per_MWh", "demand_weighted_market_price_GBP_per_MWh"):
        baseline = zonal.loc["scenario_0", metric]
        zonal[f"delta_{metric}"] = zonal[metric] - zonal.index.get_level_values("zone").map(baseline)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    summary.to_csv(args.output_dir / "scenario_summary.csv", float_format="%.9f")
    zonal.to_csv(args.output_dir / "zonal_metrics.csv", float_format="%.9f")
    checksum = hashlib.sha256(args.archive.read_bytes()).hexdigest()
    print(f"Archive SHA-256: {checksum}")
    print(summary[["delta_operating_cost_million_GBP", "delta_variable_RES_curtailment_TWh", "cost_delta_per_added_dispatched_tidal_GBP_per_MWh"]].round(4).to_string())
    print(f"Saved scenario_summary.csv and zonal_metrics.csv to {args.output_dir.resolve()}")


if __name__ == "__main__":
    main()
