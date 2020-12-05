import os 

class flight_path(object):
    """ 
    a helper class to set a sequence of camera views to generate a flight path. 
    
    see ../aspect_mesh_source.py for example usage.
    """
    def __init__(self,auto_build = True, frame_offset = 0):
        self.anchor_points = []
        self.anchor_keys = ('steps_from_previous','cam_position','cam_width','north_vector','focus')
        self.flight_path = []
        self.auto_build = auto_build  # rebuild flight path automatically when adding anchor point 
        self.frame_offset = frame_offset 
        
    def _validate_new_anchor(self,new_anchor): 
        # checks for required anchor keys, if any keys are None, will set current anchor 
        # point equal to previous anchor point for that key 
        missing = [key for key in self.anchor_keys if key not in new_anchor.keys()]
        if len(missing):
            raise ValueError(f"new anchor point missing keys: {missing}")
        
        if new_anchor['steps_from_previous'] == 0: 
            raise ValueError(f"steps_from_previous must be > 0")

        if len(self.anchor_points):
            old_anchor = self.anchor_points[-1] 
            for key,val in new_anchor.items():
                if val is None: 
                    new_anchor[key] = old_anchor[key]         
        return new_anchor
                    
    def add_anchor(self, steps_from_previous=2,cam_position=None,cam_width=None,north_vector=None,focus=None):
        """ adds an anchor point to flight path

        Parameters
        ----------
        steps_from_previous : int
            number of increments between this point and previous (the default is 2).
        cam_position : array-like
            the position to move to
        cam_width : array-like
            the camera width to move to
        north_vector : array-like
            the north vector to move to
        focus : array-like
            the focus point of the camera

        
        all of the arrays should be length 3. Anything not specified will pull the previous anchor 
        point's value. 
        """
              
        new_point = (steps_from_previous,cam_position,cam_width,north_vector,focus)
        new_anchor = dict(zip(self.anchor_keys,new_point))
        self.anchor_points.append(self._validate_new_anchor(new_anchor))
        if len(self.anchor_points) > 1 and self.auto_build:
            self._build_flight_path()
        
    def _build_flight_path(self): 
        # builds a flight path from the anchor points
        if len(self.anchor_points) <= 1: 
            raise ValueError("at least 2 anchor_points are required.")
        
        starting_point = self.anchor_points[0]
        starting_point['frame'] = 1 + self.frame_offset 
        self.flight_path = [starting_point,]
        a_keys = self.anchor_keys
        for anchor_id, anchor in enumerate(self.anchor_points):
            if anchor_id == 0: 
                continue

            old_a = self.anchor_points[anchor_id-1]
            dsteps = anchor['steps_from_previous']
            dvals = dict(zip(a_keys,[(anchor[ky] - old_a[ky])/dsteps for ky in a_keys]))
            for flight_step in range(dsteps):
                pt0 = self.flight_path[-1]
                new_point = dict(zip(a_keys,[pt0[ky] + dvals[ky] for ky in a_keys]))
                new_point['frame'] = pt0['frame'] + 1 
                self.flight_path.append(new_point)


class flight_animator(object):
    '''
    given a yt scene and a flight_path, will step through and render each frame. 
    
    see ../aspect_mesh_source.py for example usage.
    
    Parameters
        ----------
        yt_scene : a yt scene            
        flight_path : a list of dicts
            a list of sequential camera settings. each element should be a dictionary with the
            the following keys: ('frame','cam_position','cam_width','north_vector','focus'). 
            Can generate this list with the mesh_animator.flight_path class            
        base_name : str
            filename base for each frame (default 'mesh_source_')
        save_dir : str
            directory to save to (default './')
        resolution : tuple
            resolution to save each frame at (default (400,400)).
        sigma_clip : None or float
            if not None, gets passed to sc.save('savename.png',sigma_clip = sigma_clip)
            default is None.
            
    after instantiating, call flight_animator.render() to render all frames. 
    '''
    def __init__(self, yt_scene, flight_path, base_name = 'mesh_source_', save_dir='./', resolution = (400,400), sigma_clip = None):
        self.sc = yt_scene
        self.save_dir = save_dir
        self.base_name = base_name
        self.flight_path = flight_path
        self.resolution = resolution
        self.sigma_clip = sigma_clip
        self.zfill_digs = 5        
        self.frame_offset = min([pt['frame'] for pt in flight_path])
        
    def render(self):
        """ steps through and renders each frame of the flight path """ 
        cam = self.sc.camera
        cam.resolution = self.resolution
        total_frames = len(self.flight_path)
        for pt in self.flight_path:
            print(f"\nRendering frame {pt['frame']-self.frame_offset} of {total_frames}")
            frame_name = self.base_name + str(pt['frame']).zfill(self.zfill_digs) + '.png'
            save_name = os.path.join(self.save_dir,frame_name)
            cam.set_position(pt['cam_position'], pt['north_vector'])
            cam.set_width(pt['cam_width'])
            cam.focus = pt['focus']
            if self.sigma_clip:
                self.sc.save(save_name, sigma_clip = self.sigma_clip)
            else:
                self.sc.save(save_name)
            