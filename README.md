# Tidal stream generation in Great Britain

Materials supporting the research paper **“An integrated framework for evaluating tidal stream generation potential and its power system benefits: evidence from Great Britain”**.

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

The published maps are accessible in a web browser without installing QGIS.

## Stage 2: Power-system modelling

Five scenarios are represented:

* Scenario 0: baseline.
* Three scenarios representing zonal tidal stream deployment in different zones.
* A full tidal deployment scenario.

## Reproduction and solvers

The original simulations used IBM ILOG CPLEX. Reference outputs are stored in `initial_results/`.

HiGHS is the intended open-source alternative for reproduction. CPLEX requires a suitable installation and licence.

Python, PyPSA, solver versions and dependencies are documented with the code. New simulation runs will write to a separate output folder to preserve the original reference results.

## Associated paper

**Title:** An integrated framework for evaluating tidal stream generation potential and its power system benefits: evidence from Great Britain

**Authors:** Daniil Hulak, Marko Aunedi, Sobhan Naderian and Gareth Taylor

**Journal, publication year and DOI:** To be added following publication.
