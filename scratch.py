
from matplotlib import pyplot as plt
import numpy as np
from numpy.linalg import svd
from smooth_rad_avg import radial_cbf_smooth

foldername = "/Users/benjaminbarad/Documents/Projects/xray_thermometer/_test/DATA"

air_reference = "/Users/benjaminbarad/Documents/Projects/xray_thermometer/_test/DATA/c1t3/sample_279K_11111eV_300mm_0_00008.cbf"

filenames = [ "c2t1/sample_260K_11111eV_300mm_0_00001.cbf", "c2t1/sample_260K_11111eV_300mm_0_00002.cbf",
 "c2t1/sample_260K_11111eV_300mm_0_00003.cbf",
 "c2t2/sample_260K_11111eV_300mm_0_00001.cbf", "c2t2/sample_260K_11111eV_300mm_0_00002.cbf",
 "c2t2/sample_260K_11111eV_300mm_0_00003.cbf","c2t2/sample_260K_11111eV_300mm_0_00004.cbf",
 "c1t2/sample_273K_11111eV_300mm_0_00001.cbf", "c1t2/sample_273K_11111eV_300mm_0_00002.cbf",
 "c1t2/sample_273K_11111eV_300mm_0_00003.cbf","c1t2/sample_273K_11111eV_300mm_0_00004.cbf", 
 "c1t2/sample_273K_11111eV_300mm_0_00005.cbf", "c1t2/sample_273K_11111eV_300mm_0_00006.cbf", 
 "c1t2/sample_273K_11111eV_300mm_0_00007.cbf","c1t2/sample_273K_11111eV_300mm_0_00008.cbf",
 "c1t2/sample_273K_11111eV_300mm_0_00009.cbf","c1t2/sample_273K_11111eV_300mm_0_00010.cbf",
 "c1t3/sample_279K_11111eV_300mm_0_00001.cbf","c1t3/sample_279K_11111eV_300mm_0_00002.cbf", 
 "c1t3/sample_279K_11111eV_300mm_0_00003.cbf","c1t3/sample_279K_11111eV_300mm_0_00004.cbf",
 "c1t3/sample_279K_11111eV_300mm_0_00005.cbf","c1t3/sample_279K_11111eV_300mm_0_00006.cbf",
 "c1t3/sample_279K_11111eV_300mm_0_00007.cbf","c1t3/sample_279K_11111eV_300mm_0_00008.cbf",
 "c1t3/sample_279K_11111eV_300mm_0_00009.cbf","c1t3/sample_279K_11111eV_300mm_0_00010.cbf",
 "c1t4/sample_280K_11111eV_300mm_0_00001.cbf", "c1t4/sample_280K_11111eV_300mm_0_00002.cbf",
 "c1t4/sample_280K_11111eV_300mm_0_00003.cbf", "c1t4/sample_280K_11111eV_300mm_0_00004.cbf",
 "c1t4/sample_280K_11111eV_300mm_0_00005.cbf", "c1t4/sample_280K_11111eV_300mm_0_00006.cbf",
 "c1t4/sample_280K_11111eV_300mm_0_00007.cbf", "c1t4/sample_280K_11111eV_300mm_0_00008.cbf",
 "c1t4/sample_280K_11111eV_300mm_0_00009.cbf","c1t4/sample_280K_11111eV_300mm_0_00010.cbf",
 "c1t2/sample_ambient_11111eV_300mm_0_00001.cbf", "c1t2/sample_ambient_11111eV_300mm_0_00002.cbf", 
 "c1t2/sample_ambient_11111eV_300mm_0_00003.cbf", "c1t2/sample_ambient_11111eV_300mm_0_00004.cbf",
 "c1t2/sample_ambient_11111eV_300mm_0_00005.cbf", "c1t2/sample_ambient_11111eV_300mm_0_00006.cbf", 
 "c1t2/sample_ambient_11111eV_300mm_0_00007.cbf","c1t2/sample_ambient_11111eV_300mm_0_00008.cbf", 
 "c1t2/sample_ambient_11111eV_300mm_0_00009.cbf","c1t2/sample_ambient_11111eV_300mm_0_00010.cbf",


 ]

reference = radial_cbf_smooth(air_reference)
vectors = []
for file in filenames:
	filename = "{}/{}".format(foldername, file)
	data = radial_cbf_smooth(filename)
	scalar = max(reference)/max(data)
	data_air_scaled = data * scalar
	data_air_subtracted = data_air_scaled - reference
	# plt.plot(data_air_subtracted, label=file)
	data_water_scalar = sum(data_air_subtracted[250:]) #*range(250,len(data_air_subtracted))
	data_water_scaled = data_air_subtracted/data_water_scalar
	vectors.append(data_air_subtracted[250:])
	# plt.plot(vectors[-1]-vectors[0])

# plt.legend()
u,s,v = svd(vectors, full_matrices=False)
fig, ax = plt.subplots()
i = 0
for vector in v.tolist()[0:3]:
	# print vector
	# ax.plot(range(len(vectors)), [value+i for value in vector], "-")
	ax.plot([value+i*0.3 for value in vector], "-")
	i+=1

fig.savefig("svd.png")

fig2, ax2 = plt.subplots()
i = 0
for vector in u.transpose().tolist()[0:2]:
	# print vector
	# ax.plot(range(len(vectors)), [value+i for value in vector], "-")
	# x = [i*0.025 for i in range(len(vector))]	
	ax2.plot([value/u.transpose().tolist()[0][index]+i*0.3 for index,value in enumerate(vector)], "-", label = "v{}".format(i)) #
	i+=1
plt.legend()
	
fig2.savefig("result.png")
fig3, ax3= plt.subplots()
ax3.plot([np.log(i) for i in s][0:2], "-")


# plt.show()

# plt.show()

