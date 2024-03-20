## Production Code

__production_main.py__

### Runs Production communications
Daily Functions:

* forms.pull_records_from_db() (Runs the Funding Forms/Guides)
* scl.run_selection_con_letter() (Selection Confirmation letters)
* lof.run_loss_funding() (Loss of Funding),
* mav_main.mav_auto_begin() (Mav campaigns),
* cfr.collect_smartsheet_requests() (Requested Client Funding Guides),
* cfr.in_prod_requests() (Process the zip file from SUN for Client Funding Guides),
* daily_mc_update.run()


### Prerequisites
This code is written in Python3 and depends on the following packages:
* numpy, scipy, pandas, matplotlib, lmfit, xarray, netCDF4, imageio, fortranformat, eomaps, h5py, shapely, geopy, pytables

Code required packages will be automatically installed after running the installation command. The code has been tested using Python version 3.8-3.10 and it is recommended to use `pyenv` or `Miniconda` to manage the Python environment.

It is also necessary to compile the radiative transfer code under `/rt_code/rt_code/` sub-directory. A sample makefile using GNU Fortran compiler (gfortran) is provided and gfortran version 12.2.0 was used for testing.

### Installation
From the code directory, run:

   `$ pip install --user -e .`

## Usage

The top-level programs contained in this repository are:
* __RTSim.py__: a driver for the doubling-adding vector radiative transfer code (not included in this repository). It offers flexible ways to create custom input files and can automatically plot the output.
* __inversion_oil.py/inversion_snow.py__: an implementation of the Levenberg-Marquardt algorithm, designed to retrieve descriptive parameters of an Earth-system scene, via an inversion of synthetic or real optical measurements of the Stokes vector (i.e., the intensity and polarization of light).
* __RSP_transect_retrieval.py__: a program to perform multiple inversions along a flight transect of the RSP sensor. Slurm is utilized for multithreading the inversions. 

Further explanation for these programs and those contained in the `src` directory can be found below:

### /src:

__GRL_snow_retrieval.py__
Snow inversions over data subsampled from Greenland

__atm_surf_params.py__
Initializes the default values of the atmosphere and surface which are used to run the RT code.

__combine_hdf.py__
Combines the output files generated from inversions for each scan block by RSP\_transect\_retrieval.py into one HDF. This file can be run automatically within a bash script or manually after a retrieval is finished.

__image_retrieval_oil.py__
Runs inversions across pixels of a 2D HARP-2 image. To activate the script, the corresponding bash file should be run (image_retrieval.s).

__inversion_config.py__
The configuration file for the inversion. The user must specify the data to invert with the filename and dataType (synthetic, RSP (new L1C/old L1B), PM, e_GAP, HARP2, etc.,). The “measurement vector” is selected through “switches". For each channel available from the lists determined by datatype, use:
* *switch_I* to select whether (1) or not (0) to use the total reflectance
* *switch_polarization* to select whether to use no polarization (0), the DoLP (1), or the polarized reflectance (2)
* *switch_oil_detection* to select the special “oil mode”, in which the DoLP is only used for angles containing sunglint contamination. 
The list of parameters to be retrieved (the “state vector”) is selected by setting the “vary” attribute to True for each desired free parameter, e.g.: freeParams["Windspeed"].vary = 1. The starting value (“first guess”) is set through the “value” attribute.

__inversion_oil.py__
Contains the main code to run an inversion, based on the settings in inversion_config.py.
The parameter evolution history will be saved as `inversion_iteration_values.txt` and `inv_iteration_plot.png`. The retrieval fit to the measurement will be saved as `inversion_gif.gif`. All files mentioned above can be found under the working directory (`/rt_code/rt_code_work_test/`). The values of the free parameters at each iteration are also printed on the screen, as well as the final fit. inversion_oil.py drives the code to form the residual which is passed to LMfit to minimize.

__inversion_snow.py__
Same as inversion_oil.py but uses extra steps and different functions to create the residual for snow. The snow inversion also contains if statements specific to when dataType = 4 (PM files).

__RSP_transect_retrieval.py__
Runs the inversion for an entire RSP file (or a portion of it). To activate the script, the corresponding bash file should be run (RSP\_transect\_retrieval.). The user must specify in inversion_config.py the desired start and end scans, and the number of scans used to average the data. The standard deviation of the average can be used as the measurement uncertainty for the inversion.

__RTSim.py__
Flexible driver for the radiative transfer code, allowing additional functionality such as plotting outputs. The program takes input files (found in directory `~/rt_code/rt_code/info`) that describe a specific scene, runs the radiative transfer code, and outputs the Intensity, DoLP, and polarized reflectance as a function of the viewing zenith angles of an RSP-like instrument, i.e., roughly +-60 deg along a meridional plane of given azimuth relative to the Sun. The input files specify parameters such as the type and amount of aerosols, the observational wavelengths, the type of surface, etc. A detailed description of each input parameter can be found in `~/rt_code/rt_code/README.txt`. Outputs are generated as [outputfile].rsp and are plotted using plot_stokes.py. To run RTSim, run the command:

   `$ python RTSim.py [input_file_name]`

The input file must exist in the `/rt_code/rt_code/info` directory.

The input can be provided as (i) traditionally formatted “info” files, as explained in the separate README file (`~/rt_code/rt_code/README.txt`); (ii) outputs obtained by using create\_rt_input\_files.py; and (iii) JSON files (link to sample JSON here). 

If no input file is provided, RTSim will run a standard scene, defined by default values within the args for Atmo() and Srf() classes in create\_rt\_input\_files.py. The simulation corresponds to an ocean scene with a wind speed of 5 m/s, a clear atmosphere (neither aerosols nor gasses are present), a solar Zenith Angle equal to 30°, and along the principal plane of reflection (relative azimuth = 0°) at the following seven RSP wavelengths: 410, 470, 555, 670, 870, 1590, 2260 nm.

The following arguments are available to RTSim:

*custom* (Flag; first position)
if no input file is provided and the custom flag is used in its place, RTSim will run by taking custom atmospheric and surface inputs provided in general\_rt\_params.py. E.g.:
`$ python RTSim.py custom <additional flags>` (replace the input file)

*nosurf* (Flag; any position)
If set, the vec_srf program used to create surface output files will not run. This will result in an error if surface output files corresponding to the atmospheric input files are not created beforehand. E.g.:
`$python RTSim.py <info file, json file or 'custom'> nosurf`

*plot/noplot* (Variable: Main function. Flag: any position)
(Boolean). If set to True, the output will be plotted. This argument is primarily used to test the functionality of code executed before the forward calculation is called. It is a variable that can be changed manually, however, the plot flag can be used in any position which will set plot to False. E.g.:
`$ python RTSim.py <info_file> noplot`

*runRTC* (Variable: Main function. Flag: any position)
(Boolean). If True, the RT code is run; if False, the code is not run. Used for testing purposes, for example, to plot an already existing output file, and can be manually changed in the main function.

*interp* (Variable: Main function. Flag: any position)
If set to 1, the meridional plane is uniform in cosine(zenith). If set to 0, the meridional plane is uniform in zenith angle. By default interp is taken from inversion_config.py, however can be set manually in the main function. In addition the interp flag can be used in any position, if the flag is provided interp will be set to 1 else 0. E.g.: 
`$ python RTSim.py <info_file or None> interp`

*taurep* (Variable: Main function. Flag: any position)
If set to 0, the aerosol amounts in the input file are interpreted as number concentrations for each species and each layer. If set to 1, those values are interpreted as optical depths referenced to the first wavelength in the list. By default taurep is taken from inversion_config.py, but it can be manually set in the main function. In addition the taurep flag can be used in any position, if the flag is provided taurep wil be set to '1' else '0'. E.g.:
`$python RTSim.py <info_file or None> taurep`

*surf_kernel* (Variable: Main function. Flag: any position)
Should be set to 0. This ensures that the surface BRDF is physical with any negative values being set equal to zero. To generate kernel files for the different classes of surface scattering the kernel_flag should be set to 1 so that negative values are allowed. Can be manually edited in the main function.

#### /src/lib:

__absorption_profile.py__
Returns the monochromatic absorption optical depth profile of the atmosphere given the wavelength, pressure layers, and the column concentration of ozone (xo3col), nitrogen dioxide (xno2col), and precipitable water vapor (xh2ocol). The column concentrations can be retrieved from MERRA-2 files (see merra2intorsp.py for instructions). To generate the absorption profile (TAUABS), the function call is TAUABS = absorption_profile(DELP, xo3col, xno2col, xh2ocol, wavelength).

__altitude_to_pressure.py__
Converts a list of desired altitudes (in meters) to the corresponding pressure layers (DELP) used by the radiative transfer code, based on the barometric formula. If a MERRA-2 HDF file is provided in the function call, the pressure layers are instead pulled from there. To generate a list of pressure layers (DELP) from a list of altitudes (alt\_list) the correct function call is DELP = altToPressure(alt\_list). The function assumes a ‘US Standard’ Atmosphere with TOA at 86km, other atmosphere types (atm\_type) are polar winter (atm\_type = polar\_winter) and polar summer (atm\_type = polar winter).

__collocate_MERRA2_RSP.py__
Uses the RSP group's account (lines #323 and #324 in V001) on earthdata.nasa.gov to poll, download, and read the MERRA-2 file(s) corresponding to a given RSP file. Three MERRA-2 files are downloaded; a 2-d file with total column amounts ("inst1\_2d\_asm\_Nx"), a 3-d file of output variables ("merra-2 inst3\_3d\_asm\_Nv"), and a 3-d file with variables used inside of the MERRA-2 model ("merra-2 tavg3\_3d\_nav\_Ne"). Additionally, an HDF is created that stores all of the downloaded MERRA-2 variables and time, latitude and longitude from the RSP file. Run this from the command line of the location of the merra2intorsp.py file: $ python collocate\_MERRA2\_RSP.py {location of RSP file} {directory of where the MERRA-2 files will be downloaded} {directory of where the new HDF will be created}

__constants.py__
Contains the get\_sensor\_wavelength function which, given the dataType, returns the sensor wavelengths, the real part of the refractive index for water, the imaginary part of the refractive index for water, the real part of the refractive index for ice, and the imaginary part of the refractive index for ice.

__coxmunk.py__
contains helper functions that define the angular region corresponding to sunglint-contaminated observations. The getGlintRegion function takes arrays of the data’s DoLP (DoLP), the Cox and Munk DoLP (DoLP\_CM), viewing zenith angle (VZA), and index of maximum intensity (specularidx) and returns the first angle (index) and the number of consecutive angles after it (span) of the sunglint. There are also optional keys to define the threshold of the DoLP (DoLP\_threshold), minimum number of angles (nangles\_min), and the VZA threshold (VZA\_threshold). The optional keys default to values used to define the glint region in synthetic and RSP data. The correct call for the function is: index, span = getGlintRegion(DoLP, DoLP\_CM, VZA, specularidx)

__create_rt_input_files.py__
Creates atmospheric and surface input files in the format required by the radiative transfer code, by applying the createAtmo() and createSrf() methods to the atmo() and srf() classes (which contain the descriptive parameters). The errorCatchingInfo and errorCatchingSrf check whether the inputs given to .createAtmo() and .createSrf() are valid.

__general_rt_params.py__
Same as atm\_surf\_params.py but is called by create\_rt\_input\_files.py and RTSim.py when no input file is specified.

__ice_scattering_files.py__
Contains the twoColRead function that reads the "two column" scattering files, the twoColWrite function that writes the "two column" scattering files, createScatMatr which creates the full scattering matrices used by the RTC, and mixCrystals which "mixes" the column and plate ice crystals of equivalent aspect ratios.

__interp_snow_scattering_matrices.py__
Contains functions that generate scattering matrix files that are interpolated to real number values of aspect ratio, roughness, and effective radius outside of a fixed grid of values of these variables. The genPolArray function accepts a point to be interpolated to (interpolant), arrays of aspect ratio, roughness, and effective radius that comprise the fixed grid (AR, D, Reff), and a fileName to save the output scattering matrix.

#### /src/plot:

__plot_inversion_iterations.py__
Plots retrieval parameters at each iteration of an inversion using .txt files generated from running inversion\_oil.py.

__plot_MERRA2_profiles.py__
Plots the profiles for MERRA-2 total precipitable water vapor, column ozone, and mid-level pressure values corresponding to transects listed in Ottaviani et al. (2019).

__plot_RSP_transect_retrievals.py__
Plots inversion results of the X1 and X2 transects from Ottaviani et al. (2019), comparing different LMFIT minimization methods: Dogbox, Trust-region reflective, Levenberg-Marquardt, and least squares.

__plot_stokes.py__
Plots any type of inversion input or radiative transfer code output file with three different plot options (1) panel RI, Rp, DoLP vs. VZA, (2) RI and DoLP vs VZA or (3) I, Q, U vs. VZA. Also contains the code that creates the inversion GIF (using plot option 1), netcdf output, and parameter values vs. iteration plot.

__plot_RAZ.py__
Plots inversions results for one scan block, varying the relative azimuth angle.

__replicate_O19fig4.py__
Recreates Figure 4 from Ottaviani et al. (2019). 

__replicate_O19fig6.py__
Recreates Figure 6 from Ottaviani et al. (2019). Iterates through ten transects (both L1B old format and L1C) and plots the retrieved parameters from RSP\_transect\_retrieval.py. The output HDF files are then used to create a histogram for the refractive indices of the transects, grouped by campaign.

__replicate_O19fig7.py__
Recreates Figure 7 from Ottaviani et al. (2019). Takes a MODIS file (the MODIS file should be subsampled to the ROI; otherwise EOMaps takes too long to load), X1 transect HDF (created by running RSP\_transect\_retrieval.py), X2 transect HDF (created by running RSP\_transect\_retrieval.py), map projection, and enhancement boolean. Two figures are produced: `replicate_O19fig7.png` contains color-coded retrievals of the ocean surface refractive index overlaid to the MODIS image of the spill (the histogram above the colorbar indicates the frequency); `replicate_O19fig7_errorplot.png` is produced to show the retrieved parameters along the transects with the associated margin of error for each scan block.

#### /src/reader:

__read_eGAP.py__
Reads NetCDF files produced from the eGap RT code. The function read\_eGAP takes a NetCDF file and solar zenith angle and returns an xarray dataset, which contains the variables RI, Q, U, Rp, and DoLP and coordinates Wavelength, VZA, SZA, and RAZ.

__read_HARP2.py__
Reads simulated HARP-2 data. Takes a [PACE HARP-2](https://oceandata.sci.gsfc.nasa.gov/directdataaccess/Level-1C/PACE_HARP2/) L1C file, wavelength (441.9, 549.8, 669.4, or 867.8 nm), and across/along-track pixel index as input, and returns a xarray dataset. The dataset contains viewing geometries (VZA, AZI, SZA, scatang) and TOA reflectances (I, Q, U, DoLP). 670 nm cannot be merged with other wavelengths since it has 60 view angles instead of 10 for 442, 550, and 867 nm.

__read_model.py__
Reads a single output file of the RT code (e.g., “.rsp” files), and returns an xarray dataset that contains the variables RI, Q, U, Rp, AOD\_f, AOD\_c, and DoLP and the ancillary wavelength, VZA, SZA, and RAZ parameters. Multiple .rsp files can be merged into a multi-wavelength dataset using xr.merge(dataset\_list).

__read_PM.py__
Used to read merged POLDER-MODIS data. Takes a [merged POLDER-MODIS file](https://drive.google.com/file/d/1hSSvHdHxjE-YySArtlAqSk1enAw4hAVt/view?usp=share_link) (PM\_file\_path), CALIPSO/SCM file (SCM\_file\_path), wavelength, and pixel number (pxiel\_num)as inputs, and returns a xarray dataset class. Pixel number is used to locate a single pixel along a CALIPSO transect which is then classified as clear or layered. The dataset is returned only if the corresponding CALIPSO file defines the same pixel as clear. The dataset contains the reflectances and geometry variables for POLDER or MODIS. POLDER and MODIS data cannot be retrieved simultaneously since POLDER has multiple view angles while MODIS only has one.

__read_RSP.py__
Reads new format L1C RSP data. Takes a new format L1C h5 file and returns an xarray dataset, which contains the variables RI, Q, U, Rp, and DoLP and coordinates Wavelength, VZA, SZA, RAZ, SCATANG, and Scans. These quantities are averaged between the start and end scans. The standard deviations of each variable (e.g. ‘VZA\_stdev’) can be used to show uncertainty in the data.

__read_RSP_oldformat.py__
Reads old format L1B RSP data. Takes an old format L1B h5 file and returns an xarray dataset which contains the variables RI, Q, U, Rp, and DoLP and coordinates Wavelength, VZA, SZA, RAZ, SCATANG, and Scans. These quantities are averaged between the start and end scans. The standard deviations of each variable (e.g. ‘VZA\_stdev’) which can be used to show uncertainty in the data.

#### /src/test_inversions:

__create_synthetic_oil.py__
Creates the oil data used in test\_synthetic\_inversion\_oil.py.

__test_single_inversion_oil.py__
Uses pytest to validate inversion results of one scan block. Depending on a user’s python console, this script may need to be run directly from terminal.

__test_synthetic_inversion_oil.py__
Same as test\_single\_inversion\_oil.py but pulls data generated from create\_synthetic\_oil.py based on the user’s input settings within the script to run the inversion. 


## Contact
For any questions please contact Matteo Ottaviani (catullovr@hotmail.com).
