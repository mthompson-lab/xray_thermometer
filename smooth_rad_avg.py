import dxtbx
import numpy as np
from scipy.ndimage.filters import median_filter
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from scitbx.matrix import sqr, col
import scitbx.matrix as matrix

def radial_cbf_smooth(filename):
    frame = dxtbx.load(filename)
    data = frame.get_raw_data().as_numpy_array()
    detector = frame.get_detector()
    beam = frame.get_beam()

    for panel in detector:
        s0 = -1 * matrix.col(beam.get_direction())
        beam_center = col(panel.get_beam_centre_px(s0))
        pix_mm = panel.get_pixel_size()
        origin = matrix.col(panel.get_origin())

    detector_distance = s0.dot(origin)
    
    y, x = np.indices((data.shape))
    r = np.sqrt((x - beam_center[0])**2 + (y - beam_center[1])**2)
    r = r.astype(np.int)
    data_mask = np.array(data, dtype=bool)
    data_mask[data<1e-6]=False
    r=r[data_mask]
    data=data[data_mask]
    tbin = np.bincount(r.ravel(), data.ravel())
    nr = np.bincount(r.ravel())
    with np.errstate(invalid='ignore', divide='ignore'):
        radial_avg = tbin / nr
    radial_avg_smooth = median_filter(radial_avg, 50)
    print("detector distance = {}".format(detector_distance))
    plt.plot(radial_avg_smooth)
    plt.savefig("smoothed_rad_avg.png", dpi=300)
    
    return radial_avg


from sys import argv

script, filename = argv
radial_cbf_smooth(filename)

