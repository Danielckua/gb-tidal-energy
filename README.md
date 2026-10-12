# Tidal stream generation in Great Britain

Materials supporting the research paper **“An integrated framework for evaluating tidal stream generation potential and its power system benefits: evidence from Great Britain”**.

**Authors:** Daniil Hulak, Marko Aunedi, Sobhan Naderian and Gareth Taylor.

The study combines geospatial resource assessment and multi-objective site optimisation with a 17-zone PyPSA model of the 2030 Great Britain electricity system to evaluate tidal stream generation potential and its operational and economic benefits.

## Repository contents

The interactive map, five Stage 2 PyPSA notebooks and their shared hourly input dataset, and the original CPLEX reference results archive are published.

| Folder             | Contents                                                                               |
| ------------------ | -------------------------------------------------------------------------------------- |
| `stage1_maps/`     | Interactive maps presenting the spatial assessment and tidal stream deployment results |
| `stage2_pypsa/`    | Five runnable Jupyter notebooks, `Inputs_2030.csv`, setup instructions and dependencies  |
| `initial_results/` | Original CPLEX reference results archive: five scenarios, 20 hourly CSV files          |

## Interactive Research Map

**[Great Britain Tidal Energy — Interactive Research Map](https://danielckua.github.io/gb-tidal-energy/?v=20261012-default-layers)**

This interactive map presents geographical screening and multi-objective optimisation results for tidal energy site selection around Great Britain. Users can compare water-depth scenarios of **30–50 m** and **35–45 m**, explore tidal-speed and distance-to-shore criteria, and examine Pareto-optimal locations alongside geographical reference layers and GB power-system boundaries.

### Exploring the map

Open **Layers** to enable or disable geographical references, optimisation results and suitability/screening layers. The legend displays the criteria associated with each coloured layer. Zoom and pan to explore the region, and click features to view their attributes. Disable **United Kingdom – Land** when you want to reveal basemap labels beneath its opaque fill. The land reference includes Northern Ireland.

The map runs in a web browser without installing QGIS. Internet access is required for the OpenStreetMap background. The research overlays are bundled with the site.

### Data sources and attribution

The research layers are the author's supplied QGIS export of the spatial assessment and optimisation results associated with the paper above. The power-system reference uses the ETYS boundaries included in that export. Detailed source datasets, versions, processing methods and applicable redistribution terms should be documented in the accompanying paper and research package; this export does not establish a new licence for third-party research data.

The geographical basemap is **© [OpenStreetMap contributors](https://www.openstreetmap.org/copyright)**. Preserve the visible attribution and follow the [OpenStreetMap tile usage policy](https://operations.osmfoundation.org/policies/tiles/). The tile service is best-effort and no API key is needed.

### Running locally

With Python installed, run this command from the repository root:

```sh
python -m http.server 8001 --bind 127.0.0.1 --directory stage1_maps
```

Then open <http://localhost:8001/>. Use an available port if 8001 is occupied. Serve the map over HTTP rather than opening `index.html` directly from the filesystem.

### Deployment

`.github/workflows/deploy-pages.yml` deploys only `stage1_maps/` as the website root on pushes to `main` or manual workflow dispatch. PyPSA scripts and simulation outputs are excluded from the website artifact. GitHub Pages must use **GitHub Actions** as its publishing source.

## Stage 2: Power-system modelling

**[Open the Stage 2 PyPSA notebooks](stage2_pypsa/)**. The five 8,760-hour simulations are provided as separate Jupyter notebooks:

* Scenario 0: baseline with no **additional** tidal deployment (597 MW of existing tidal capacity).
* Scenario 1: additional 500 MW in zone 1.
* Scenario 2: additional 500 MW in zone 9.
* Scenario 3: additional 500 MW in zone 15.
* Scenario 4: additional 500 MW in each of zones 1, 9 and 15.

See the [Stage 2 README](stage2_pypsa/README.md) for setup, model assumptions, solver choice, run instructions and limitations.

## Reproduction and solvers

The original simulations used IBM ILOG CPLEX. The original CPLEX results are published as a **single archive**: [Download CPLEX reference results ZIP](initial_results/GB_tidal_CPLEX_reference_results.zip) (13.8 MB). After extraction, the archive contains five scenario directories and four hourly CSV outputs per scenario. See [results documentation and checksum](initial_results/README.md).

HiGHS is the default open-source solver in the published notebooks. CPLEX can be selected if its compatible Python interface and suitable licence are installed. The notebooks include an **optional**, commented pip installation cell for users who do not already have a working PyPSA environment.

New simulation results are written into separate `stage2_pypsa/outputs/<scenario>/` folders (ignored by Git) and will not overwrite the archived reference CPLEX outputs. The code has been structurally checked, but a full 8,760-hour run in a clean modern PyPSA environment has not been independently validated; exact original software and solver versions should be documented alongside the reference results.

## Associated paper

**Title:** An integrated framework for evaluating tidal stream generation potential and its power system benefits: evidence from Great Britain

**Authors:** Daniil Hulak, Marko Aunedi, Sobhan Naderian and Gareth Taylor

**Journal, publication year and DOI:** To be added following publication.
