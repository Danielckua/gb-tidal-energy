# Original CPLEX reference results

This folder contains a single compressed archive of the **original 2030 Great Britain 17-zone PyPSA power-system simulation outputs solved using IBM ILOG CPLEX** for the five scenarios reported in the associated tidal-stream generation study.

**Download:** [GB_tidal_CPLEX_reference_results.zip](GB_tidal_CPLEX_reference_results.zip) (~13.8 MB). The archive contains **20 CSV files** (five folders, four files per folder), each with **8,760 hourly observations**.

| Folder inside ZIP | Additional tidal capacity |
| --- | --- |
| `scenario_0/` | Baseline: no additional tidal deployment (597 MW existing) |
| `scenario_1_z1/` | 500 MW in zone 1 |
| `scenario_2_z9/` | 500 MW in zone 9 |
| `scenario_3_z15/` | 500 MW in zone 15 (original source file label: `z12_15`) |
| `scenario_4_all/` | 500 MW in each of zones 1, 9 and 15 |

Each folder contains:

- `pypsa_results_gen.csv`: generator dispatch by snapshot.
- `pypsa_results_stor.csv`: storage dispatch by snapshot.
- `pypsa_results_marginal_price.csv`: bus marginal prices by snapshot.
- `pypsa_results_network.csv`: network link-flow results by snapshot.

### Integrity

SHA-256 of the downloaded ZIP:

```text
890f7d7547ec84f3ed12f34a769463076a21f9ece62f9fafdd54e5de9cf9ef4a
```

All 20 CSV files were preserved without changing their numerical values. File naming within the archive has been standardised to match the published scenario terminology.

### Extraction

Download the ZIP through the link above and extract it using your operating system, or:

```bash
python -m zipfile -e GB_tidal_CPLEX_reference_results.zip .
```

The interactive maps and the corresponding **five reproducible PyPSA notebooks** are elsewhere in this repository, under `stage1_maps/` and `stage2_pypsa/`. The published notebooks default to HiGHS; these archived reference results were generated using CPLEX. Solver/package versions and numerical settings for the historic reference runs are not independently recorded in this archive; reproduced solutions may differ slightly.
