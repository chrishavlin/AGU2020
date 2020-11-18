import os,yt, numpy as np
from yt_velmodel_vis import seis_model as SM, shapeplotter as SP, transferfunctions as TFs
import matplotlib.pyplot as plt

def build_yt_scene(ds, datafld, model, bbox):
    """ builds the yt scene:

    - Draws the spherical chunk bounding the dataset
    - Draws a latitude/longitude grid at surface
    - Draws shapefile data: US political boundaries, tectonic boundaries, volcanos

    """

    # create the scene (loads full dataset into the scene for rendering)
    sc = yt.create_scene(ds, datafld)

    # add useful annotations to the scene in two parts: 1. Domain Annotations and 2. Shapefile Data

    # 1. Domain Annotations :
    # define the extent of the spherical chunk
    lat_rnge = [np.min(model.data.variables['latitude']), np.max(model.data.variables['latitude'])]
    lon_rnge = [np.min(model.data.variables['longitude']), np.max(model.data.variables['longitude'])]
    Depth_Range = [0, 1200]
    R = 6371.
    r_rnge = [(R - Depth_Range[1]) * 1000., (R - Depth_Range[0]) * 1000.]

    # create a spherical chunk object
    Chunk = SP.sphericalChunk(lat_rnge, lon_rnge, r_rnge)

    # add on desired annotations to the chunk
    sc = Chunk.domainExtent(sc, RGBa=[1., 1., 1., 0.002], n_latlon=100, n_rad=50)  # extent of the domain
    sc = Chunk.latlonGrid(sc, RGBa=[1., 1., 1., 0.005])  # lat/lon grid at the surface
    sc = Chunk.latlonGrid(sc, RGBa=[1., 1., 1., 0.002], radius=(R - 410.) * 1000.)  # lat/lon grid at 410 km depth
    sc = Chunk.latlonGrid(sc, RGBa=[1., 1., 1., 0.002],
                          radius=(R - Depth_Range[1]) * 1000.)  # lat/lon grid at lower extent
    sc = Chunk.wholeSphereReference(sc, RGBa=[1., 1., 1., 0.002])  # adds lines from Earth's center to surface

    # 2. Shapefile Data
    # set the surficial bounding box, used for reading all shapefiles
    shp_bbox = [lon_rnge[0], lat_rnge[0], lon_rnge[1], lat_rnge[1]]

    # US political boundaries
    thisshp = SP.shapedata('us_states', bbox=shp_bbox, radius=R * 1000.)
    sc = thisshp.addToScene(sc)

    # tectonic boundaries: buid a dictionary with unique RGBa values for each
    clrs = {
        'transform': [0.8, 0., 0.8, 0.05],
        'ridge': [0., 0., 0.8, 0.05],
        'trench': [0.8, 0., 0., 0.05],
        'global_volcanos': [0., 0.8, 0., 0.05]
    }
    for bound in ['transform', 'ridge', 'trench', 'global_volcanos']:
        tect = SP.shapedata(bound, radius=R * 1000., buildTraces=False)
        sc = tect.buildTraces(RGBa=clrs[bound], sc=sc, bbox=shp_bbox)

    return sc


def getCenterVec(bbox):
    # center vector
    x_c = np.mean(bbox[0])
    y_c = np.mean(bbox[1])
    z_c = np.mean(bbox[2])
    center_vec = np.array([x_c, y_c, z_c])
    return center_vec / np.linalg.norm(center_vec)


def setCamera(sc, bbox):
    pos = sc.camera.position

    # center vector
    center_vec = getCenterVec(bbox)
    sc.camera.set_position(pos, north_vector=center_vec)

    # zoom in a bit
    zoom_factor = 0.7  # < 1 zooms in
    init_width = sc.camera.width
    sc.camera.width = (init_width * zoom_factor)

def plotTf_yt(data,tf,dvs_min,dvs_max):
    x = np.linspace(dvs_min,dvs_max,tf.nbins) # RGBa value defined for each dvs bin in range
    y = tf.funcs[3].y # the alpha value of transfer function at each x
    w = np.append(x[1:]-x[:-1], x[-1]-x[-2])
    colors = np.array([tf.funcs[0].y, tf.funcs[1].y, tf.funcs[2].y,
                       tf.funcs[3].y]).T
    fig = plt.figure()
    ax = fig.add_axes([0.2, 0.2, 0.75, 0.75])
    d_hist=ax.hist(data['dvs'][~np.isnan(data['dvs'])].ravel(),bins=100,density=True,log=False,color='k')
    ax.bar(x, tf.funcs[3].y, w, edgecolor=[0.0, 0.0, 0.0, 0.0],
           log=False, color=colors, bottom=[0])
    plt.xlabel('$\mathregular{dV_s}$')
    plt.show()


def plotTf(tfOb):
    """ create a histogram-transfer function plot and display it"""
    f=plt.figure()
    ax=plt.axes()
    ax=tfOb.addHist(ax=ax,density=True,color=(0.,0.,0.,1.))
    ax=tfOb.addTFtoPlot(ax=ax)
    ax.set_xlabel('$\mathregular{dV_s}$')
    plt.show()


def configure_scene(ds, datafld, model, bbox, the_transfer_function, res_factor=1.):
    # build scene, apply camera settings, set the transfer function
    sc = build_yt_scene(ds, datafld, model, bbox)
    setCamera(sc, bbox)
    source = sc.sources['source_00']
    source.set_transfer_function(the_transfer_function)

    # adjust resolution of rendering
    res = sc.camera.get_resolution()
    new_res = (int(res[0] * res_factor), int(res[1] * res_factor))
    sc.camera.set_resolution(new_res)

    print("Scene ready to render")
    return sc

