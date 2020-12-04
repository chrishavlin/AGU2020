from mesh_animator import mesh_animator as MA 
import numpy as np 
import yt 
import os

ds = yt.load('aspect/fault_formation/solution-00050.pvtu')
sc = yt.create_scene(ds,('connect1','strain_rate')) # this is the slowest step 

ms = sc.get_source()
ms.cmap = 'magma'
ms.color_bounds = (1e-20,1e-14)

# now let's construct the flight path 
reload(MA)
FP0 = MA.flight_path(frame_offset = 5)

# first anchor must have all fields
FP0.add_anchor(1,
              cam_position=ds.arr([200.0, 200.0, 200.0], 'km'),
              cam_width=ds.arr([600, 600, 600], 'km'),
              north_vector=ds.arr([0.0, 1.0, 0.0], 'dimensionless'),
              focus=ds.arr([250.0, 250.0, 50.0], 'km'),
              )
                            
# rotate north_vector
FP0.add_anchor(5,
              north_vector=ds.arr([0.0, 0., 0.1], 'dimensionless')
              )

# narrow the camera field of view (zooms in)
FP0.add_anchor(5,
              cam_width=ds.arr([300, 300, 300], 'km'),
              )

# move camera position closer to center
FP0.add_anchor(5,
              cam_position=ds.arr([200.0, 200.0, 100.0], 'km')
              )

# and move a bit closer
pos = FP0.flight_path[-1]['cam_position']*0.9
FP1.add_anchor(5, cam_position=pos)
              
# narrow the field of view a bit more
wid = FP0.flight_path[-1]['cam_width']*0.8
FP0.add_anchor(5, cam_width=wid)

# move position to side-view
FP0.add_anchor(5,
              cam_position=ds.arr([100.0, 200.0, 100.0], 'km')
              )

# move position to side-view
FP0.add_anchor(5, cam_position=ds.arr([200.0, 100.0, 100.0], 'km'))

# zoom and move closer 
pos = FP1.flight_path[-1]['cam_position']
wid = FP1.flight_path[-1]['cam_width']*.7
pos[1] = pos[1]*0.7; pos[2] = pos[2]*0.7
FP0.add_anchor(10, cam_position=pos, cam_width=wid)

# sit here for a few frames 
FP0.add_anchor(5, cam_position=pos, cam_width=wid)

# return to start 
final_pos = {key:val for key,val in FP0.flight_path[0].items() if key !='frame' and key != 'steps_from_previous'}
FP0.add_anchor(20, **final_pos)

# and sit here a bit too
FP0.add_anchor(10)

# now render it all 
save_dir = '../figures/aspect_3d'
if os.path.isdir(save_dir) is False:
    os.mkdir(save_dir)
    
FA = MA.flight_animator(sc,FP0.flight_path,base_name='aspect_mesh_',save_dir=save_dir,resolution=(1200,1200),sigma_clip = 6.)
FA.render()
