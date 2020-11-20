import yt
import os
from pvuLoder import pvuFile
import numpy as np

# set the file path 
DataDir=os.path.join(os.environ.get('ASPECTdatadir','./'),'fault_formation')
pFile=os.path.join(DataDir,'solution-00050.pvtu')
if os.path.isfile(pFile) is False:
    print(f"data file not found: {pFile}")

# instantiate our manual pvu loader and load into memory (takes a while!)
pvuData=pvuFile(pFile)
pvuData.load()

# create the yt dataset
ds = yt.load_unstructured_mesh(
    pvuData.connectivity,
    pvuData.coordinates,
    node_data = pvuData.node_data,
    length_unit="m"
)

# create a couple slices in strain rate: 
sr_cmap = 'magma'

slc = yt.SlicePlot(ds,'x',('all','strain_rate'))
slc.set_log('strain_rate',True)
slc.set_cmap(('all','strain_rate'),sr_cmap)
slc.hide_axes()
slc.save('../figures/aspect_fault_xsec.png')

c_val = ds.domain_center
c_arr = np.array([c_val[0],c_val[1],ds.domain_width[2]*0.8])
slc = yt.SlicePlot(ds,'z',('all','strain_rate'),center=c_arr)
slc.set_log('strain_rate',True)
slc.set_cmap(('all','strain_rate'),sr_cmap)
slc.hide_axes()
slc.save('../figures/aspect_fault_map.png')
