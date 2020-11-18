This repository contains some sample notebooks and code used in creating the figures for the following presentation at AGU Fall Meeting 2020:

Abstract **IN037-13**: [Visualization and Analysis of 3D Data in the Geosciences Using the yt Platform](https://agu.confex.com/agu/fm20/meetingapp.cgi/Paper/696827)

**Authors**: Christopher Havlin<sup>1</sup>, Matthew Turk<sup>1</sup>, Benjamin K Holtzman<sup>2</sup>, Leigh Orf<sup>3</sup>, Kelton Halbert<sup>3</sup>, John B Naliboff <sup>4</sup>, Kacper Kowalik<sup>1</sup>, Madicken Munk<sup>1</sup>, Sam Walkow<sup>1</sup>

1. University of Illinois at Urbana Champaign
2. Lamont Doherty Earth Observatory, Columbia Univ.
3. University of Wisconsin Madison
4. New Mexico Institute of  Mining and Technology

### Abstract

We present a number of advances to the yt platform for visualization and analysis of 3D observational and model data in the geosciences. yt is an open source, python-based package originally designed for analysis of astrophysical datasets. yt enables units-aware analysis and visualization of large 3D datasets, including 2D slices and projections, particle path analysis and 3D volume rendering. A number of recent efforts have focused on transforming yt into a more domain-agnostic tool for use beyond astrophysics through new implementations within yt itself and through connections to the wider open source ecosystem.

In this presentation, we highlight advances in using yt within the geoscience domains of atmospheric dynamics, seismic tomography and computational geodynamics. Within atmospheric dynamics, we demonstrate a new yt-native front end for CF-compliant netcdf files using 3D visualizations of supercell thunderstorms creating violent tornadoes. Within seismic tomography, we demonstrate using yt to generate 3D volume renderings of IRIS Earth Model Collaboration netcdf files that explore seismic tomography models at different lengthscales, furthering the goal of robust feature interpretation that is less dependent on hidden user choices in rendering parameters. And within computational geodynamics we demonstrate initial advances in visualizing both 2D and 3D output from the ASPECT mantle convection and lithospheric dynamics code using yt. Additionally, we present a number of new features including interactive visualization and shapefile support that help make yt a cross-domain tool for analysis and visualization in the geosciences.

## repository description

The notebooks here all require *yt* (https://yt-project.org/). Additional requirements for each notebook (including in some cases particular development branches or forks) are referenced within each notebook. 

`./notebooks/` contains the notebooks linked to by the e-Presentation. 
`./code/` contains scripts used for generating figures 
`./figures/` output directory for figures
