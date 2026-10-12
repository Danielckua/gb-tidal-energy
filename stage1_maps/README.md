# Stage 1 — tidal stream site maps

**[Open the interactive research map](https://danielckua.github.io/gb-tidal-energy/?v=20261012-default-layers)**

This Leaflet/qgis2web export shows the study's screening and multi-objective site-selection results. It corresponds to the spatial results in Figures 6–8 of the submitted paper.

## Explore the layers

The map opens with **OpenStreetMap and ETYS boundaries** enabled. Open **Layers**, select a screening or Pareto layer, then zoom into Orkney/Pentland Firth, Anglesey/North Wales or the Bristol Channel. Click a feature to inspect its attributes. Disable **United Kingdom – Land** to reveal basemap labels beneath its opaque fill.

| Layer group | Meaning |
| --- | --- |
| Geographical references | OpenStreetMap, land, coastline and ETYS boundaries |
| Screening with mean speed | Mean tidal speed ≥1.5 m/s, distance to shore ≤50 km, and the selected depth range |
| Screening with maximum and mean speed | Maximum speed ≥2.5 m/s, mean speed ≥1.5 m/s, distance to shore ≤50 km, and the selected depth range |
| Pareto-optimal sites | NSGA-II site-selection output for each depth range |

Both **30–50 m** and **35–45 m** depth ranges are available; the optimisation uses **40 m** as the reference depth. The underlying screening grid is **500 × 500 m**. The paper's static maps use 1:3,500,000 for GB and 1:215,000 for detail panels; the interactive map has variable zoom.

The optimisation treats shoreline distance, maximum current, mean current and deviation from 40 m depth as competing objectives. These are suitability results, not installed plants or turbine-level energy-yield predictions. See the [source and reproduction notes](../docs/reproducibility.md).

## Run locally

From the repository root:

```sh
python -m http.server 8001 --bind 127.0.0.1 --directory stage1_maps
```

Open <http://localhost:8001/>. Internet is needed for OpenStreetMap tiles; research overlays are bundled in `data/`. Use HTTP rather than opening `index.html` as a local file.

## Attribution and hosting

Preserve the visible **© [OpenStreetMap contributors](https://www.openstreetmap.org/copyright)** credit and follow the [tile usage policy](https://operations.osmfoundation.org/policies/tiles/): use HTTPS, allow the browser's genuine Referer, respect caching, and do not bulk-download or prefetch tiles.

The [Pages workflow](../.github/workflows/deploy-pages.yml) deploys only this folder on pushes to `main`. The model and results ZIP remain available through GitHub, outside the map website.
