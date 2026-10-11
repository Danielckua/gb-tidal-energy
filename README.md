# Tidal stream generation in Great Britain

Materials supporting the research paper **“An integrated framework for evaluating tidal stream generation potential and its power system benefits: evidence from Great Britain”**.

**Authors:** Daniil Hulak, Marko Aunedi, Sobhan Naderian and Gareth Taylor.

The study combines geospatial resource assessment and multi-objective site optimisation with a 17-zone PyPSA model of the 2030 Great Britain electricity system to evaluate tidal stream generation potential and its operational and economic benefits.

## Repository contents

The interactive map is included. The Stage 2 code, inputs and reference results listed below form the planned research package and will be added separately.

| Folder             | Contents                                                                               |
| ------------------ | -------------------------------------------------------------------------------------- |
| `stage1_maps/`     | Interactive maps presenting the spatial assessment and tidal stream deployment results |
| `stage2_pypsa/`    | Five power-system scenario scripts and supporting inputs                               |
| `initial_results/` | Reference simulation outputs produced using CPLEX                                      |

## Interactive Research Map

**[Great Britain Tidal Energy — Interactive Research Map](https://danielckua.github.io/gb-tidal-energy/)**

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

Five scenarios are planned for the power-system research package:

* Scenario 0: baseline.
* Three scenarios representing zonal tidal stream deployment in different zones.
* A full tidal deployment scenario.

## Reproduction and solvers

The original simulations used IBM ILOG CPLEX. Reference outputs are planned for `initial_results/` and are not yet included in this repository.

HiGHS is the intended open-source alternative for reproduction. CPLEX requires a suitable installation and licence.

Python, PyPSA, solver versions and dependencies will be documented with the code when the research package is released. New simulation runs will write to a separate output folder to preserve the original reference results.

## Associated paper

**Title:** An integrated framework for evaluating tidal stream generation potential and its power system benefits: evidence from Great Britain

**Authors:** Daniil Hulak, Marko Aunedi, Sobhan Naderian and Gareth Taylor

**Journal, publication year and DOI:** To be added following publication.
