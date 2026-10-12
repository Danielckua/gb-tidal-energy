# Original CPLEX reference results

**[Download GB_tidal_CPLEX_reference_results.zip](GB_tidal_CPLEX_reference_results.zip)** — 13.8 MB, five scenario folders and four hourly CSV files per folder. Each of the 20 files contains **8,760 observations**.

| Folder inside ZIP | Scenario |
| --- | --- |
| `scenario_0/` | Baseline |
| `scenario_1_z1/` | Additional 500 MW tidal in zone 1 |
| `scenario_2_z9/` | Additional 500 MW tidal in zone 9 |
| `scenario_3_z15/` | Additional 500 MW tidal in zone 15; original output label `z12_15` |
| `scenario_4_all/` | Additional 500 MW tidal in each of zones 1, 9 and 15 |

## Files in each scenario folder

| File | Contents | Units / convention |
| --- | --- | --- |
| `pypsa_results_gen.csv` | Generator dispatch | MW |
| `pypsa_results_stor.csv` | Net storage dispatch | MW; positive discharge, negative charging |
| `pypsa_results_marginal_price.csv` | Zonal marginal prices | £/MWh |
| `pypsa_results_network.csv` | Inter-zonal link flows (`p0`) | MW; positive from `bus0` to `bus1` |

Rows use one-hour snapshot indices **0–8759**. Some scenarios omit inactive zero-capacity generators, so their column counts differ.

## Extract the archive

Download the ZIP and extract it using your operating system, or run from this folder:

```sh
python -m zipfile -e GB_tidal_CPLEX_reference_results.zip .
```

The extracted files are the original CPLEX outputs. Newly generated results from the [PyPSA notebooks](../stage2_pypsa/) are saved in `stage2_pypsa/outputs/`.

## Archive integrity

SHA-256:

```text
890f7d7547ec84f3ed12f34a769463076a21f9ece62f9fafdd54e5de9cf9ef4a
```

The original numerical values are preserved; folder and file names were standardised for the published package. For interpretation and analysis of the results, refer to the associated paper and its [figures](../docs/figures/).
