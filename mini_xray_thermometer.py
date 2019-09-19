import dxtbx
import numpy as np
from scipy.ndimage.filters import median_filter
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from scitbx.matrix import sqr, col
import scitbx.matrix as matrix

import subprocess
from itertools import islice
import pandas
import StringIO
import numpy as np
from sys import argv
#import matplotlib.pyplot as plt
from glob import glob
from time import clock
from numpy.linalg import svd
import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot as plt

path = "/path/to/the/data"

list_of_filenames = []

for r, d, f in os.walk(path):
    list_of_filenames.append(os.path.join(r, f))




for filename in list_of_filenames:
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
    # plt.plot(radial_avg_smooth)
    # plt.savefig("smoothed_rad_avg.png", dpi=300)
    
    list_of_rad_averages.append(radial_avg_smooth)


fig0, ax0 = plt.subplots()

list_of_scaled_averages = []

mask_min = 
mask_max = 

ref = list_of_rad_averages[0]

for curve in list_of_rad_averages:
    
    data_mask = np.array(curve, dtype=bool)
    data_mask[curve<mask_min]=False
    data_mask[curve>mask_max]=False
    masked_curve = curve[data_mask]
    masked_ref = ref[data_mask]
    top = np.dot(masked_ref,masked_ref)
    bottom = np.dot(masked_ref,masked_curve)
    scalar = top/bottom
    scaled_curve = masked_curve*scalar
    ax0.plot(range(len(scaled_curve)), scaled_curve)
    list_of_scaled_averages.append(scaled_curve)
    
fig0.savefig("rad.png")


u,s,v = svd(list_of_scaled_averages, full_matrices=False)
fig, ax = plt.subplots()
i = 0
#print("xx shape = {}".format(xx.shape))
for vector in v[0:8]:
    # print vector
    #print("vector shape = {}".format(vector.shape))
    # ax.plot(range(len(vectors)), [value+i for value in vector], "-")
    ax.plot(x[cutoff:],vector+i*0.1, "-", label = "v{}".format(i))
    i+=1
plt.legend()
#fig.savefig("{}_svd.png".format(run_numb))
fig.savefig("singular_vectors.png", dpi=300)

#np.save("time_dep_vector", v[2])

fig2, ax2 = plt.subplots()
i = 0
for vector in u.T[0:8]:
    # print vector
    # ax.plot(range(len(vectors)), [value+i for value in vector], "-")
    # x = [i*0.025 for i in range(len(vector))] 
    ax2.scatter(dark, vector[dark]+i*.3, color='blue', edgecolors="none", s=2, label = "v{} dark".format(i))
    ax2.scatter(light, vector[light]+i*.3, marker='+', color='red', edgecolors="none", s=2, label = "v{} light".format(i))
    i+=1
#plt.legend()
    
#fig2.savefig("{}_result.png".format(run_numb))
fig2.savefig("vector_per_image.png", dpi=300)
fig2.set_figwidth(15)
fig3, ax3= plt.subplots()
ax3.plot([np.log(i) for i in s][0:8], "-")
#fig3.savefig("{}_singular_values.png".format(run_numb))
fig3.savefig("singular_values.png")
#plt.show(figsize(10,10),dpi=300)
    # print i
    # print ordered_keylist
#fig2.show()
fig4, ax4 = plt.subplots()
i = 0
for vector in u.T[0:8]:
    # print vector
    # ax.plot(range(len(vectors)), [value+i for value in vector], "-")
    # x = [i*0.025 for i in range(len(vector))] 
    ax4.hist(vector[dark], 500, color='blue', alpha=0.5, label = "v{} dark".format(i))
    ax4.hist(vector[light], 500, color='red', alpha=0.5, label = "v{} light".format(i))
    plt.legend()
    fig4.savefig("v{}_distribution.png".format(i), dpi=300)
    i+=1
    ax4.cla()
