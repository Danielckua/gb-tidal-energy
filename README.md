# Tidal stream generation in Great Britain

Research materials supporting **“An integrated framework for evaluating tidal stream generation potential and its power system benefits: evidence from Great Britain”**.

**Authors:** Daniil Hulak, Marko Aunedi, Sobhan Naderian and Gareth Taylor.

The study combines geospatial resource assessment and multi-objective site optimisation with a 17-zone PyPSA model of the 2030 Great Britain electricity system to evaluate tidal stream generation potential and its operational and economic benefits.

## Repository contents

| Folder             | Contents                                                                               |
| ------------------ | -------------------------------------------------------------------------------------- |
| `stage1_maps/`     | Interactive maps presenting the spatial assessment and tidal stream deployment results |
| `stage2_pypsa/`    | Five power-system scenario scripts and supporting inputs                               |
| `initial_results/` | Reference simulation outputs produced using CPLEX                                      |

## Stage 1: Interactive maps

The maps present the spatial assessment of tidal currents, water depth, distance to shore and candidate deployment locations.

**Online map:** Link to be added after deployment.

The published maps will be accessible in a web browser without installing QGIS.

## Stage 2: Power-system modelling

Five scenarios are planned for inclusion:

* Scenario 0: baseline.
* Three scenarios representing zonal tidal stream deployment.
* A full tidal deployment scenario.

Exact scenario identifiers, input requirements and execution instructions will be added with the scripts.

## Reproduction and solvers

The original simulations used IBM ILOG CPLEX. Reference outputs will be stored in `initial_results/`.

HiGHS is the intended open-source alternative for reproduction. Compatibility and results will be checked before HiGHS instructions are marked as tested. CPLEX requires a suitable installation and licence.

Python, PyPSA, solver versions and dependencies will be documented with the code. New simulation runs will write to a separate output folder to preserve the original reference results.

## Associated paper

**Title:** An integrated framework for evaluating tidal stream generation potential and its power system benefits: evidence from Great Britain

**Authors:** Daniil Hulak, Marko Aunedi, Sobhan Naderian and Gareth Taylor

**Journal, publication year and DOI:** To be added following publication.

## Data sources and reuse

Dataset references, acknowledgements and applicable reuse terms will be documented alongside the uploaded materials. Third-party datasets retain their original licence terms.

## Current status

Repository under preparation. Maps, scenario scripts, reference results and reproduction instructions are being added.
