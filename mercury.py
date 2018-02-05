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



cutoff = 400

indexed_shots_only = argv[1]
if indexed_shots_only == "indexed":
	indexed = True
else:
	indexed = False
directs = argv[2:]

light_dark_map = {"/r0016/": "light", "/r0034/": "light", "/r0039/": "dark", "/r0040/": "dark", "/r0044/": "light", "/r0045/": "light", "/r0046/": "light", "/r0047/": "dark", "/r0048/": "dark", "/r0049/": "dark", "/r0066/": "light", "/r0067/": "light", "/r0068/": "light", "/r0072/": "dark", "/r0073/": "light", "/r0074/": "light", "/r0075/": "light", "/r0076/": "dark", "/r0077/": "light", "/r0078/": "dark", "/r0079/": "light", "/r0080/": "dark", "/r0081/": "light", "/r0082/": "dark", "/r0083/": "light", "/r0084/": "dark", "/r0085/": "light", "/r0086/": "light", "/r0087/": "dark"}



directories = [str(direct)+"002_*/out/debug" for direct in directs] #003 specifies trial - rg Aaron rungroup with latest metrology - for spot finding
hitlist = set(line.strip() for line in subprocess.check_output("sh /reg/d/psdm/mfx/mfxls2116/scratch/common/xray_thermometer/generate_hitlist.sh {}".format(directories[0]), shell=True).split())
for dir_x in directories[1:]:
   hitlist.update(line.strip() for line in subprocess.check_output("sh /reg/d/psdm/mfx/mfxls2116/scratch/common/xray_thermometer/generate_hitlist.sh {}".format(dir_x), shell=True).split())
print(hitlist)

g_directs = [str(direct)+"003_*/stdout" for direct in directs] #002 specifies trial - Aaron run group with latest metrology - for radial averaging
#run_numb = g_direct.split('/')[-3] 

from glob import glob
def logfiles(directory):
    log_list = glob(directory+"/*log_rank*")
    print log_list
    return log_list

list_of_filenames = []
for g_dir in g_directs:
    list_of_filenames.extend(logfiles(g_dir))

start = clock()

n = 1381
i = 0
# filename = '28565-dark1.txt'
#list_of_filenames = ['28570-dark1.txt', '28570-dark2.txt','28570-light.txt']
#list_of_filenames = ['28965-dark1.txt', '28965-dark2.txt','28965-light.txt']
#list_of_filenames = filelist(in_dir)
#list_of_filenames = ['./28566-dark1.txt', './28566-dark2.txt', './28566-light.txt', './28567-dark1.txt', './28567-dark2.txt', './28567-light.txt', './28568-dark1.txt', './28568-dark2.txt', './28568-light.txt', './28569-dark1.txt', './28569-dark2.txt', './28569-light.txt', '28570-dark1.txt', '28570-dark2.txt','28570-light.txt']
panda_dict = {}
ordered_keylist = []
#n = 1376
#i = 0
#for filename in list_of_filenames:
#  with open(filename) as f:
  #  header = list(islice(f, 2))
 #   while True:
  #      next_n_lines = list(islice(f, n))
 #       i +=1
#	if len(next_n_lines)<10:
        #  break
  #      print next_n_lines[1]   
       # if next_n_lines[1].split()[1] in hitlist:
        #if next_n_lines[1].split()[1] not in hitlist:
        #  print(next_n_lines)
        #  print map(str.split, next_n_lines[4:])
        #  dataset = pandas.DataFrame(map(str.split, next_n_lines[6:]), columns = ["q", "I", "sigI"], dtype=float)
for filename in list_of_filenames:
		with open(filename) as f:
		    header = list(islice(f,2))
		    #print header
		    while True:
		        next_n_lines = list(islice(f, n))
		        i +=1
			if len(next_n_lines)<10:
			    break
		        #print next_n_lines[1]
		        #print len(map(str.split, next_n_lines[6:]))
			# if i>1:
		        try:
				if indexed == True: 
					#print "using indexed images only"
					if next_n_lines[3].split()[1] in hitlist:
						dataset = pandas.DataFrame(map(str.split, next_n_lines[8:-2]), columns = ["q", "I", "sigI"], dtype=float)
		        			for item in light_dark_map:
							if item in filename:
								panda_dict[i] = [dataset, light_dark_map[item]]
		        			ordered_keylist.append(i)
						print("{} succeeded, and was '{}'".format(i, panda_dict[i][1]))
					elif next_n_lines[1].split()[1] not in hitlist:
						print("{} not indexed".format(i))
				elif indexed == False:
						#print "using all images"
						dataset = pandas.DataFrame(map(str.split, next_n_lines[8:-2]), columns = ["q", "I", "sigI"], dtype=float)
                                                for item in light_dark_map:
                                                        if item in filename:
                                                                panda_dict[i] = [dataset, light_dark_map[item]]
						ordered_keylist.append(i)
						print("{} succeeded, and was '{}'".format(i, panda_dict[i][1]))
			except:	
				print("{} failed".format(i))
			# 	break
		        	
		        #if len(next_n_lines)<10:
		         #   break

		  #      print next_n_lines[1]   
		        # if next_n_lines[1].split()[1] in hitlist:
		        #if next_n_lines[1].split()[1] not in hitlist:
		        #  print(next_n_lines)
		        #  print map(str.split, next_n_lines[4:])
fig0, ax0 = plt.subplots()
# for key in panda_dict:
# 	ax.plot(panda_dict[key].q, panda_dict[key].I)
# fig.savefig("rad.png")



full_list = []
lab_list = []

x = panda_dict[ordered_keylist[0]][0]["q"].values
refy = panda_dict[ordered_keylist[0]][0]["I"].values
for key in panda_dict:
	y = panda_dict[key][0]["I"].values
	lab = panda_dict[key][1]
	# print(y.max())
	try:
		#scalar = np.divide(refy.max(),y.max())
		data_mask = np.array(x, dtype=bool)
		data_mask[x<2.0]=False
		data_mask[x>2.5]=False
		yy = y[data_mask]
		refyy = refy[data_mask]
		xx = x[data_mask]
		q_ref = xx*refyy
		q_sig = xx*yy
		top = np.dot(q_sig,q_ref)
		bottom = np.dot(q_sig,q_sig)
		scalar = top/bottom
		temp = y*scalar
		temp2 = temp - temp.min()
		temp3 = np.divide(temp2,temp2.max())
		# print temp3.shape
		ax0.plot(x, temp3)
		full_list.append(temp3[cutoff:])
		lab_list.append(lab)
	except:
		print "{} failed".format(key)

fig0.savefig("rad.png")
dark_coor = []
light_coor = []
for i, val in enumerate(lab_list):
	if val == "dark":
		dark_coor.append(i)
	elif val == "light":
		light_coor.append(i)

dark = np.array(dark_coor)
light = np.array(light_coor)

#dark_vecs = np.array([full_list[d] for d in dark])
#light_vecs = np.array([full_list[l] for l in light])
#avg_dark = np.average(dark_vecs,axis=0)
#diff = light_vecs - avg_dark

end = clock()
print("calculation finished in {} seconds").format(end-start)
print("vectors processed = {}").format(len(full_list))

u,s,v = svd(full_list, full_matrices=False)
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
	

#u_d,s_d,v_d = svd(diff, full_matrices=False)

#fig5, ax5 = plt.subplots()
#i = 0
#for vector in v_d[0:8]:
        # print vector
        # ax.plot(range(len(vectors)), [value+i for value in vector], "-")
        #ax.plot(vector+i*0.1, "-", label = "v{}".format(i))
        #i+=1
#plt.legend()
#fig.savefig("{}_svd.png".format(run_numb))
#fig5.savefig("singular_diff_vectors.png", dpi=300)

#fig6, ax6 = plt.subplots()
#ax6.plot([np.log(i) for i in s_d][0:8], "-")
#fig3.savefig("{}_singular_values.png".format(run_numb))
#fig6.savefig("singular_diff_values.png")
