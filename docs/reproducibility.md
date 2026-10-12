# Sources, reproduction and paper consistency

This package accompanies the manuscript **“An integrated framework for evaluating tidal stream generation potential and its power system benefits: evidence from Great Britain”**, submitted to *Energy*. The consistency check uses the supplied `Tidal project paper_final_draft - no highlights.docx` and repository materials as available on **12 October 2026**. The manuscript itself is not published in this repository.

## Sources and coverage

| Material | Source or assumption reported in the manuscript | Supplied here |
| --- | --- | --- |
| Bathymetry and coastline | GEBCO_2025; 15 arc-second source bathymetry | Derived map layers; no raw bathymetry |
| Tidal resource | TPXO9-atlas-v5; 960 hourly snapshots over 40 days; interpolation to a 500 m grid | Derived screening and Pareto map layers; no raw tidal fields or MATLAB preprocessing |
| Spatial processing | QGIS 3.40.12, EPSG:27700, 500 × 500 m grid | Browser-ready qgis2web export; no native QGIS project or processing model |
| Site selection | NSGA-II, PyMoo 0.6.1.6 | Pareto outputs; optimisation code, settings and seeds are not supplied |
| GB zones and transmission | ETYS 2024 boundaries, boundary capacities and contracted generation | Exported boundaries and notebook component definitions |
| 2030 generation and demand | FES 2025 Holistic Transition and 2030/2031 winter peak | Fixed notebook capacities, regional shares and processed demand |
| Demand shape | NESO 2023 national hourly profile, scaled to the future peak | `Inputs_2030.csv` |
| Wind and PV profiles | Renewables.ninja; coordinates in manuscript Annex A | Processed hourly availability columns |
| Tidal generation profiles and costs | Literature source cited in manuscript | Processed hourly tidal profiles and notebook costs; not regenerated from the mapped sites |
| Geographical context | OpenStreetMap contributors | Online basemap with visible attribution |
| Reference simulations | CPLEX, five configurations | Original ZIP, 20 hourly CSVs and a derived summary |

The two spatial depth scenarios are **35–45 m** and **30–50 m**, with a 40 m reference depth. These are distinct from the five power-system deployment scenarios. A spatial layer locates suitable sites; the power-system notebooks apply zonal capacities and supplied profiles. There is no automated map-to-notebook data pipeline in this package.

## Consistency with the submitted paper

The model and reference archive are preserved. Documentation describes the implementation supported by those files rather than silently changing it to match conflicting manuscript statements.

| Item | Manuscript | Supplied implementation / check |
| --- | --- | --- |
| Baseline tidal | Methodology describes a case with no tidal generation | Annex B and Scenario 0 include 597 MW: 287 in z1, 100 in z9 and 210 in z10. Interpret the baseline as no **additional** deployment. |
| Wind substitution in z1 | Table 4: −100 MW onshore, −302 MW offshore | Scenarios 1 and 4 remove **100 MW offshore and 302 MW onshore**. Baseline offshore capacity is only 100 MW. |
| Wind substitution in z12 | Table 4: −81 MW offshore | Scenarios 3 and 4 remove **81 MW onshore** in z12. Added tidal is in z15. |
| Energy equivalence | PV coefficient 0.3 in the methodology and 0.4 in Table 4's caption | Notebooks apply fixed capacity changes. Available annual RES energy is not exactly identical across scenarios. The illustrative 0.5 GW at 40% CF equals **1.667 GW**, not 1.25 GW, at 12% CF. |
| Interconnectors | Described as capacity-constrained links | International imports are aggregated generator proxies at **£250/MWh**. Only inter-zonal GB corridors are `Link` components. No export decision or foreign-price time series is supplied. |
| RES curtailment | Baseline 85.84 TWh; combined reduction about 0.69 TWh | Available generation minus archived dispatch gives **85.8301 TWh** baseline and **85.2889 TWh** combined: a **0.5412 TWh** reduction. The rounded values/plot and narrative need reconciliation. |
| Tidal curtailment and SIC | Tidal curtailment described as negligible; Table 5: −13.9, −14.3, −11.0, −17.6 £/MWh for combined, z1, z9, z15 | Available and dispatched tidal increments differ. The summary reports cost changes per both denominators, without claiming exact reproduction of Table 5. For the combined case, available energy gives **−12.27 £/MWh** and dispatched energy gives **−13.85 £/MWh**. |
| Original software | PyPSA 1.0.4, Python 3.10, CPLEX 22.1 | The published [PyPSA 1.0.4 metadata](https://pypi.org/project/pypsa/1.0.4/) requires **Python ≥3.11**. Notebook kernel metadata names Python 3.10.19; original runtime records are needed to reconcile these statements. |

The archived operating-cost reduction for the combined scenario is **£64.9693 million/year**, supporting the paper's approximately £65 million finding. The summary code calculates costs using all generator components in the model objective and prices using explicit generation or demand weights. It is a new transparent analysis utility, not the unavailable original figure-generation script.

## Validation and software

Completed for this update:

- All five notebooks are valid JSON; their code compiles and active profile references exist in the shared input file.
- All five models build with 17 buses, 16 links and 23 storage units. Nuclear, storage and capacity substitutions were inspected against the manuscript.
- A **48-hour Scenario 0** optimisation with HiGHS returned `ok / optimal`; PyPSA's curtailment calculation also succeeded. This is a short functional check, not an annual result reproduction.
- All 20 reference CSVs have 8,760 finite hourly rows indexed 0–8759. The archive checksum matches the previously published value. The summary utility validates generator/price column sets and dispatch against available capacity.
- Relative documentation links and local map dependencies were checked. The existing map code and its two default visible layers were retained.

The construction and short optimisation checks used **Python 3.12.14, PyPSA 1.0.4, linopy 0.10.0, highspy 1.15.1, pandas 3.0.6 and NumPy 2.5.4**. These model-package versions are recorded in `stage2_pypsa/requirements.txt`; JupyterLab is an additional notebook interface. Linopy emitted a warning about future handling of absent storage-state slots; the check used its current default semantics. The original CPLEX environment, complete transitive dependency lockfile and numerical settings are not supplied.

Full-year reruns, reconstruction of Stage 1 from raw data and exact regeneration of Figures 11–12 have not been validated in this update. For an exact reproduction, retain the original environment/solver log, supply the missing spatial and post-processing scripts, and reconcile the differences above. New model outputs are kept separate from the archived reference data.

## Attribution and reuse

The map credits **© [OpenStreetMap contributors](https://www.openstreetmap.org/copyright)** and uses the public tile service subject to its [usage policy](https://operations.osmfoundation.org/policies/tiles/). Derived research layers do not confer a new licence on GEBCO, TPXO, NESO, Renewables.ninja or other third-party data; check their source terms before redistribution.

[Selected manuscript figures](figures/README.md) are copied unchanged from the supplied DOCX with their figure numbers and source identified. This update does not introduce a blanket licence for the paper, code or datasets. Use the citation metadata and record the repository commit when referring to this package; replace the manuscript citation with the published DOI when available.
