# LGM-Pattern-Effect

This repository documents the creation of the sst and sea-ice boundary conditions for the paleo pattern effect simulations with HadGEM3-GC3.1-LL.

Tim Andrews

Met Office Hadley Centre.

Jan 2023

## Data files

The ancillary files have been produced using `create_ancs.py`. In a nutshell it uses existing ancillary files (in this case `sst_piControl18501899clim_n96e.anc` and `ice_piControl18501899clim_n96e.anc` from HadGEM3-GC3-1.LL RFMIP simulations) as target model grid/attributes, then interpolates the data to this. The time-coordinate has to be adjusted to work with the UM's 360day calendar with continuous time increments. Sea-ice outside of 0 to 100% are reset and % converted to a fraction 0 to 1.

| Original Filename | HadGEM3-GC3.1-LL Ancillary file |
| -------- | ----------- |
| `holo_sst_bc.nc` | `holo_sst.anc` |
| `holo_ice_bc.nc` | `holo_ice.anc` |
| `lgm_sst_bc.nc` | `lgm_sst.anc` |
| `lgm_ice_bc.nc` | `lgm_ice.anc` |
| `2x_sst_bc.nc` | `2x_sst.anc` |
| `2x_ice_bc.nc` | `2x_ice.anc` |

Note the ancillary files also have `.nc` versions.
