# imports and initialization
import os
import sys
import yt
import matplotlib.pyplot as plt
from yt_velmodel_vis import seis_model as SM, transferfunctions as TFs


sys.path.append(os.path.abspath("../notebooks/resources"))
import seismic_helper as SH

###################
# volume rendering
###################

# load interpolated data using the yt uniform grid loader (not editable)
# set the model file and the field to visualize
modelfile='NWUS11-S_percent.nc' # the model netCDF file
datafld='dvs' # the field to visualize, must be a variable in the netCDF file

# set the interpolation dictionary. If the interpolation for this model does
# not exist, SM.netcdf() will build it.
interp_dict={'field':datafld,'max_dist':50000,'res':[10000,10000,10000],
              'input_units':'m','interpChunk':int(1e7)}

# load the model
model=SM.netcdf(modelfile,interp_dict)

# set some objects required for loading in yt
bbox = model.cart['bbox'] # the bounding box of interpolated cartesian grid
data={datafld:model.interp['data'][datafld]} # data container for yt scene

# load the data as a uniform grid, create the 3d scene
ds = yt.load_uniform_grid(data,data[datafld].shape,1.0,bbox=bbox,nprocs=1,
                        periodicity=(True,True,True),unit_system="mks")

# setting up transfer functions
tfOb = TFs.dv(data[datafld].ravel(), bounds=[-4, 4])

# segment 1, slow anomalies
bnds = [-1.3, -.3]
TFseg = TFs.TFsegment(tfOb, bounds=bnds, cmap='OrRd_r')
alpha_o = 0.95
Dalpha = -0.85
alpha = alpha_o + Dalpha / (bnds[1] - bnds[0]) * (TFseg.dvbins_c - bnds[0])
tfOb.addTFsegment(alpha, TFseg)

# segment 2, fast anomalies
bnds = [.1, .35]
TFseg = TFs.TFsegment(tfOb, bounds=bnds, cmap='winter_r')
alpha_o = .6
Dalpha = .4
alpha = alpha_o + Dalpha / (bnds[1] - bnds[0]) * (TFseg.dvbins_c - bnds[0])
tfOb.addTFsegment(alpha, TFseg)

# build the scene
sc = SH.configure_scene(ds, datafld, model, bbox, tfOb.tf,res_factor=5)

sc.save('../figures/seismic_vol_render_highres.png',sigma_clip=1.5)

