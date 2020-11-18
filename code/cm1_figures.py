# reproduces the volume rendering from the cm1_supercell notebook at a higher
# resolution -- will take a while to run.

import yt
ds = yt.load('cm1_tornado_lofs/budget-test.04400.000000.nc')

# standard vol rending
sc = yt.create_scene(ds,'dbz')

# Get a reference to the VolumeSource associated with this scene
# It is the first source associated with the scene, so we can refer to it
# using index 0.
source = sc[0]

# first let's specify the bounds
bounds = (20,60)
source.tfh.set_bounds(bounds)

# and specify the field and whether or not to work in log space:
source.set_field('dbz')
source.set_log(False)
sigma_clip_val = 3

# now let's instantiate a transfer function with 5 guassian layers:
tf = yt.ColorTransferFunction(bounds)
tf.add_layers(5, colormap='arbre')
source.tfh.tf = tf
# source.tfh.bounds = bounds

# zoom in
zoom_factor = 0.25 # < 1 zooms in
init_width = sc.camera.width
sc.camera.width = (init_width * zoom_factor)

# set up
pos = sc.camera.position
sc.camera.set_position(pos, north_vector=[0, 0, -1])

# let's up the resolution (will slow things down!)
res_factor = 5
res = sc.camera.get_resolution()
new_res = (int(res[0]*res_factor), int(res[1]*res_factor))
sc.camera.set_resolution(new_res)

# finally save it (will render in process)
sc.save('../figures/cm1_vol_render_highres.png',sigma_clip = sigma_clip_val)

