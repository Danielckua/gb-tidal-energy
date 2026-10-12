# Stage 2 — 2030 GB power-system scenarios

Five independent notebooks build the published 17-zone model and optimise **8,760 one-hour snapshots**. Each uses the same processed `Inputs_2030.csv`; no data API or API key is needed.

## Run a scenario

Use **Python 3.11 or later**; Python 3.12 was used for the repository checks. From the repository root:

```sh
cd stage2_pypsa
python -m venv .venv
```

Activate the environment:

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

```sh
# macOS / Linux
source .venv/bin/activate
```

Then install and open Jupyter:

```sh
python -m pip install -r requirements.txt
jupyter lab
```

Open a notebook, select this environment's kernel, and run cells from top to bottom. Keep the working directory in `stage2_pypsa/`, beside `Inputs_2030.csv`. If you already have a working compatible environment, skip installation. The optional installation cell remains commented out.

Each notebook sets `SOLVER = "highs"`. To use the paper's solver, set `SOLVER = "cplex"` and install a compatible licensed IBM CPLEX Python interface separately. Full-year runs can take substantial time and memory. Record the installed versions and solver settings with your results.

## Capacity substitutions

These are the **actual notebook changes relative to Scenario 0**, in MW. They retain the supplied model configuration; Table 4 of the manuscript has different wind-type labels in zones 1 and 12.

| Notebook | Added tidal | Removed wind / PV | Total tidal capacity |
| --- | --- | --- | ---: |
| [scenario_0.ipynb](scenario_0.ipynb) | None | None | 597 |
| [scenario_1_z1.ipynb](scenario_1_z1.ipynb) | 500 in z1 | 100 offshore wind + 302 onshore wind in z1 | 1,097 |
| [scenario_2_z9.ipynb](scenario_2_z9.ipynb) | 500 in z9 | 527 PV + 258 offshore wind in z9 | 1,097 |
| [scenario_3_z15.ipynb](scenario_3_z15.ipynb) | 500 in z15 | 1,310 PV in z15 + 81 onshore wind in z12 | 1,097 |
| [scenario_4_all.ipynb](scenario_4_all.ipynb) | 500 each in z1, z9, z15 | All three substitutions above | 2,097 |

The baseline tidal portfolio is **287 MW in z1, 100 MW in z9 and 210 MW in z10**. These are baseline capacities assumed for 2030, not a statement about currently operating plants. The original `z12_15` output label refers to tidal deployment in z15 and wind substitution in z12.

## Model assumptions

| Element | Implementation in the notebooks |
| --- | --- |
| Network | 17 GB buses and 16 bidirectional, capacity-constrained `Link` corridors; no transmission losses |
| Demand | Shared national hourly profile multiplied by fixed zonal shares |
| Wind, PV and tidal | Fixed capacities, supplied availability profiles, zero marginal cost |
| Conventional generation | Fixed capacities and constant marginal costs; nuclear minimum output 50% |
| Interconnectors | Aggregated import-only `Generator` components at £250/MWh, not foreign buses or bidirectional interconnector links |
| Battery storage | Two hours; 90% efficiency each way; initially empty |
| Pumped hydro | Plant-specific 4–20 hour durations; 80% charging and 93% discharging efficiency; initially 50% full |
| Storage boundary | No cyclic end-of-year state-of-charge constraint; no charging/discharging marginal cost |
| Load shedding | Backup generator in each zone at £3,000/MWh |
| Decisions | Continuous dispatch and storage scheduling with fixed asset capacities; no capacity expansion or unit commitment |

The link network is a zonal transport representation. It does not implement AC power flow or line impedances. See [the system map and topology](../docs/figures/README.md) and [paper/code consistency notes](../docs/reproducibility.md).

## Outputs

New runs write to `outputs/<scenario>/`, ignored by Git:

| File | Contents and units |
| --- | --- |
| `pypsa_results_gen.csv` | Generator dispatch, MW; includes imports and load shedding |
| `pypsa_results_stor.csv` | Net storage power, MW; positive discharge, negative charging |
| `pypsa_results_marginal_price.csv` | Zonal marginal prices, £/MWh |
| `pypsa_results_network.csv` | Link `p0`, MW; positive from `bus0` to `bus1` |
| `pypsa_inputs_gen.csv` | Generator parameters for the run |
| `pypsa_inputs_stor.csv` | Storage parameters for the run |
| `curtailment_results.csv` | PyPSA curtailment summary, MWh for one-hour snapshots |

Snapshots are integer labels **0–8759**, not timestamped observations from calendar year 2030. Preserve the supplied row order.

The original CPLEX results are in a [separate ZIP](../initial_results/). For comparisons without a solver, use [summarise_results.py](summarise_results.py) and its [instructions](../initial_results/README.md#summarise-without-a-solver).

## Validation

All five models were constructed with PyPSA 1.0.4. A **48-hour baseline** solved optimally with HiGHS and the curtailment export succeeded. A full-year rerun has not been performed in this audit. Eight inactive baseline generator definitions with missing input columns remain commented out; they have zero installed capacity. [Versions and remaining reproduction gaps](../docs/reproducibility.md#validation-and-software).
