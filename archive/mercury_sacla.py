import subprocess
from itertools import islice
import pandas
import StringIO
import numpy as np
from sys import argv
import matplotlib.pyplot as plt
from glob import glob
from time import clock
from numpy.linalg import svd


#script, in_dir = argv
list_of_filenames = argv[1:]
def filelist(directory):
    log_list = glob(directory+"*txt")
    print log_list
    return log_list


start = clock()

n = 1189
i = 0
# filename = '28565-dark1.txt'
#list_of_filenames = ['28570-dark1.txt', '28570-dark2.txt','28570-light.txt']
#list_of_filenames = ['28965-dark1.txt', '28965-dark2.txt','28965-light.txt']
#list_of_filenames = filelist(in_dir)
#list_of_filenames = ['./28566-dark1.txt', './28566-dark2.txt', './28566-light.txt', './28567-dark1.txt', './28567-dark2.txt', './28567-light.txt', './28568-dark1.txt', './28568-dark2.txt', './28568-light.txt', './28569-dark1.txt', './28569-dark2.txt', './28569-light.txt', '28570-dark1.txt', '28570-dark2.txt','28570-light.txt']
panda_dict = {}
ordered_keylist = []
for filename in list_of_filenames:
	if 'dark' in filename:
		with open(filename) as f:
		    # header = list(islice(f, 16))
		    # print header
		    while True:
		        next_n_lines = list(islice(f, n))
		        i +=1
		        # print next_n_lines[16:-1]
		        # if i>1:
		        dataset = pandas.DataFrame(map(str.split, next_n_lines[17:-1]), columns = ["q", "I", "sigI"], dtype=float)
		        panda_dict[i] = [dataset, "dark"]
		        ordered_keylist.append(i)
		        # 	break
		        	
		        if len(next_n_lines)<10:
		            break

	elif 'light' in filename:
		with open(filename) as f:
		    # header = list(islice(f, 16))
		    # print header
		    while True:
		        next_n_lines = list(islice(f, n))
		        i +=1
		        # print next_n_lines[16:-1]
		        # if i>1:
		        dataset = pandas.DataFrame(map(str.split, next_n_lines[17:-1]), columns = ["q", "I", "sigI"], dtype=float)
		        panda_dict[i] = [dataset, "light"]
		        ordered_keylist.append(i)
		        # 	break
		        	
		        if len(next_n_lines)<10:
		            break
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
		full_list.append(temp3[400:])
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

end = clock()
print("calculation finished in {} seconds").format(end-start)
print("vectors processed = {}").format(len(full_list))

u,s,v = svd(full_list, full_matrices=False)
fig, ax = plt.subplots()
i = 0
for vector in v[0:8]:
	# print vector
	# ax.plot(range(len(vectors)), [value+i for value in vector], "-")
	ax.plot(vector+i*0.1, "-", label = "v{}".format(i))
	i+=1
plt.legend()
#fig.savefig("{}_svd.png".format(run_numb))
fig.savefig("singular_vectors.png", dpi=300)

np.save("time_dep_vector", v[2])

fig2, ax2 = plt.subplots()
i = 0
for vector in u.T[0:8]:
	# print vector
	# ax.plot(range(len(vectors)), [value+i for value in vector], "-")
	# x = [i*0.025 for i in range(len(vector))]	
	ax2.scatter(dark, vector[dark]+i*.3, s=1, label = "v{} dark".format(i))
	ax2.scatter(light, vector[light]+i*.3, s=1, label = "v{} light".format(i))
	i+=1
plt.legend()
	
#fig2.savefig("{}_result.png".format(run_numb))
fig2.savefig("vector_per_image.png", dpi=300)
fig3, ax3= plt.subplots()
ax3.plot([np.log(i) for i in s][0:8], "-")
#fig3.savefig("{}_singular_values.png".format(run_numb))
fig3.savefig("singular_values.png")
#plt.show(figsize(10,10),dpi=300)
	# print i
	# print ordered_keylist

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
	
