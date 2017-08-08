
from matplotlib import pyplot as plt
import numpy as np
from numpy.linalg import svd
from smooth_rad_avg import radial_cbf_smooth

foldername = "/Users/benjaminbarad/Documents/Projects/xray_thermometer/_test/DATA/c1t2"

air_reference = "/Users/benjaminbarad/Documents/Projects/xray_thermometer/_test/DATA/c1t2/background_ambient_11111eV_300mm_0_00006.cbf"

filenames = ["sample_273K_11111eV_300mm_0_00001.cbf", "sample_273K_11111eV_300mm_0_00002.cbf",
 "sample_273K_11111eV_300mm_0_00003.cbf","sample_273K_11111eV_300mm_0_00004.cbf", 
 "sample_273K_11111eV_300mm_0_00005.cbf", "sample_273K_11111eV_300mm_0_00006.cbf", 
 "sample_273K_11111eV_300mm_0_00007.cbf","sample_273K_11111eV_300mm_0_00008.cbf",
 "sample_273K_11111eV_300mm_0_00009.cbf","sample_273K_11111eV_300mm_0_00010.cbf",
 "sample_ambient_11111eV_300mm_0_00001.cbf", "sample_ambient_11111eV_300mm_0_00002.cbf", 
 "sample_ambient_11111eV_300mm_0_00003.cbf", "sample_ambient_11111eV_300mm_0_00004.cbf",
 "sample_ambient_11111eV_300mm_0_00005.cbf", "sample_ambient_11111eV_300mm_0_00006.cbf", 
 "sample_ambient_11111eV_300mm_0_00007.cbf","sample_ambient_11111eV_300mm_0_00008.cbf", 
 "sample_ambient_11111eV_300mm_0_00009.cbf","sample_ambient_11111eV_300mm_0_00010.cbf"]

reference = radial_cbf_smooth(air_reference)
vectors = []
for file in filenames:
	filename = "{}/{}".format(foldername, file)
	data = radial_cbf_smooth(filename)
	scalar = max(reference)/max(data)
	data_air_scaled = data * scalar
	data_air_subtracted = data_air_scaled - reference
	plt.plot(data_air_subtracted, label=file)
	data_water_scalar = sum(data_air_subtracted[250:])
	data_water_scaled = data_air_subtracted/data_water_scalar
	vectors.append(data_air_subtracted)
	# plt.plot(vectors[-1]-vectors[0])

plt.legend()
u,s,v = svd(vectors, full_matrices=False)
fig, ax = plt.subplots()
i = 0
for vector in v.tolist()[0:3]:
	# print vector
	# ax.plot(range(len(vectors)), [value+i for value in vector], "-")
	ax.plot([value+i*0.3 for value in vector], "-")
	i+=1


fig2, ax2 = plt.subplots()
i = 0
for vector in u.transpose().tolist()[0:3]:
	# print vector
	# ax.plot(range(len(vectors)), [value+i for value in vector], "-")
	x = [i*0.025 for i in range(len(vector))]	
	ax2.plot(x, [value+i for value in vector], "-")
	i+=0.3
	
fig3, ax3= plt.subplots()
ax3.plot([np.log(i) for i in s][0:3], "-")


plt.show()

# plt.show()

