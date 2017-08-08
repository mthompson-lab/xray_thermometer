import subprocess
directory = "/reg/d/psdm/mfx/mfxo1916/scratch/tmp_training/results/r0020/000_rg001/out/debug"
print set(line.strip() for line in subprocess.check_output("sh generate_hitlist.sh {}".format(directory), shell=True).split())
