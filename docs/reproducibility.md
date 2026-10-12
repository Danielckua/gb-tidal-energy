# Data sources and reproduction

This guide describes the materials accompanying the tidal stream generation study. The paper provides the full methodology, assumptions and interpretation of the results.

## Sources and coverage

| Research element | Source or software | Materials in this repository |
| --- | --- | --- |
| Bathymetry and coastline | GEBCO_2025 | Derived spatial map layers |
| Tidal resource | TPXO9-atlas-v5 | Derived tidal-current screening layers |
| Spatial processing and site selection | QGIS 3.40.12; NSGA-II with PyMoo 0.6.1.6 | Interactive screening and Pareto-optimal site maps |
| GB network and 2030 portfolio | ETYS 2024 and FES 2025 Holistic Transition | Zonal network, capacities and demand shares in the notebooks |
| Hourly demand | NESO 2023 demand profile scaled to the future peak | Processed `Inputs_2030.csv` |
| Wind and PV availability | Renewables.ninja | Processed hourly profiles in `Inputs_2030.csv`; coordinates in paper Annex A |
| Tidal availability and generator costs | Literature sources identified in the paper | Processed tidal profiles and notebook cost assumptions |
| Power-system modelling | PyPSA; reference simulations solved with CPLEX | Five notebooks, shared inputs and original hourly output ZIP |
| Geographical basemap | OpenStreetMap contributors | Online basemap with visible attribution |

Stage 1 uses a **500 × 500 m grid**, depth ranges of **35–45 m** and **30–50 m**, and a **40 m** reference depth. These spatial alternatives are separate from the five Stage 2 power-system deployment scenarios.

The package supplies the browser-ready map export, model notebooks and processed hourly inputs. Raw GEBCO/TPXO data, the native QGIS project, and spatial preprocessing/NSGA-II scripts are not included. The [paper figures](figures/) illustrate the framework and results.

## Software and running the model

Use the [Stage 2 setup guide](../stage2_pypsa/) and `requirements.txt` to install the model environment. The published notebooks default to **HiGHS**; **CPLEX** requires a separately installed, compatible Python interface and licence.

All five models have been checked for construction with PyPSA 1.0.4, and a 48-hour baseline test solved with HiGHS. This was a functional check; the original full-year CPLEX outputs are provided in the [reference archive](../initial_results/). A different solver or environment may produce differences in dispatch and prices.

## Attribution

Preserve **© [OpenStreetMap contributors](https://www.openstreetmap.org/copyright)** on the maps and follow the [OpenStreetMap tile usage policy](https://operations.osmfoundation.org/policies/tiles/). Source datasets retain their own redistribution terms; this repository does not establish a new licence for third-party data.

The selected figures are from the associated paper by Daniil Hulak, Marko Aunedi, Sobhan Naderian and Gareth Taylor. The publication citation and DOI will be added once available.
