# Stage 2 — 2030 GB power-system scenarios (PyPSA)

Five independent Jupyter notebooks reproduce the 17-zone dispatch-model configurations used in the study. Their component definitions, network topology, time-series inputs, and original data/assumptions have been retained. A standalone notebook and the shared `Inputs_2030.csv` are sufficient to build each scenario.

## Scenarios

| Notebook | Added tidal capacity | Total tidal capacity |
| --- | --- | ---: |
| `scenario_0.ipynb` | No **additional** tidal capacity | 597 MW |
| `scenario_1_z1.ipynb` | 500 MW in zone 1 | 1,097 MW |
| `scenario_2_z9.ipynb` | 500 MW in zone 9 | 1,097 MW |
| `scenario_3_z15.ipynb` | 500 MW in zone 15 | 1,097 MW |
| `scenario_4_all.ipynb` | 500 MW each in zones 1, 9 and 15 | 2,097 MW |

The baseline includes 287 MW in zone 1, 100 MW in zone 9 and 210 MW in zone 10, totaling **597 MW of existing tidal capacity**. “No tidal” refers to no additional deployment, **not** zero tidal production. The original notebook filename containing `z12_15` actually deploys added capacity in **zone 15 only**.

## Setup

- **For a new environment, Python 3.12 is recommended.** Current PyPSA (1.x) supports Python 3.11+; the original notebooks retain their historical Python 3.10.19 kernel metadata, which does **not** indicate validation against PyPSA 1.x. Select an available compatible Python kernel in Jupyter if your local environment name differs.
- If PyPSA and the supporting packages are already installed in a working environment, **skip the optional installation cell** in each notebook. Do not upgrade a working environment solely to follow this guide.
- For a **new** environment, run the commented command in the optional first code cell once, or install from `requirements.txt`:

  ```bash
  python -m pip install -r requirements.txt
  jupyter lab
  ```

- The simplified, unpinned requirements install current compatible package releases. PyPSA installs **HiGHS** as its default open-source solver. Users choosing **CPLEX** must install the IBM CPLEX Python interface separately and have an appropriate licence for a full-year model. Python 3.12-compatible CPLEX distributions are available, but compatibility of this particular research model with a new PyPSA/CPLEX stack has **not** been fully validated.
- Keep `Inputs_2030.csv` beside the notebooks and run cells from top to bottom. This is a full-year **8,760-hour** optimisation, which may be computationally demanding.
- Each notebook prints the installed PyPSA version for the run record. Record your Python version, installed dependency versions, solver/version and solver settings alongside reproduced results. The original paper results used CPLEX; installing the newest package releases does not guarantee identical outputs.

## Solver selection

Each notebook starts with the setting:

```python
SOLVER = "highs"  # default: free and open source
```

For the original IBM CPLEX route, change the setting to `SOLVER = "cplex"`. **CPLEX is not installed by this package.** Users must separately install IBM CPLEX and its compatible Python interface, and ensure they have a valid licence. Solver availability is checked immediately before optimisation; missing solver installations trigger a clear error.

The paper's original optimisation results were produced with CPLEX. HiGHS solves the same formulated model but may yield small differences owing to numerical tolerances, alternative optimal solutions, or solver settings. The original CPLEX outputs are released **separately** in [`initial_results/GB_tidal_CPLEX_reference_results.zip`](../initial_results/GB_tidal_CPLEX_reference_results.zip); these notebooks do **not** overwrite them.

## Outputs

New runs write seven CSV files per scenario to `stage2_pypsa/outputs/<scenario>/`:

- `pypsa_results_gen.csv` — generator dispatch
- `pypsa_results_stor.csv` — storage dispatch
- `pypsa_results_marginal_price.csv` — bus marginal prices
- `pypsa_results_network.csv` — link flows (`p0`)
- `pypsa_inputs_gen.csv` — generator component inputs
- `pypsa_inputs_stor.csv` — storage component inputs
- `curtailment_results.csv` — curtailment summary using the original method

The outputs directory is intentionally excluded from Git. The reference CPLEX results are supplied as a ZIP archive in the repository's separate [`initial_results/`](../initial_results/) folder.

## Limited fix to baseline scenario

Eight **zero-capacity** generator definitions in the original Scenario 0 notebook referred to profile columns absent from `Inputs_2030.csv`. Those eight definitions are now **commented out and preserved next to their original positions**, preventing `KeyError` while leaving installed capacity and effective generation unchanged. All other component definitions are preserved.

## Validation status

The notebooks have been structurally checked (valid JSON, Python code compilation, field references and file-path isolation). **No full 8,760-hour PyPSA/HiGHS/CPLEX optimisation has been executed in this preparation environment.** Before scientific release, run representative model construction and at least one full optimisation in a suitable Python environment; record solver and package versions with the reference outputs.
