import sys, os
import numpy as np
from scipy.stats import ttest_rel
from numpy import genfromtxt

NUM_SIMULATIONS = 31
NUM_RANKS = 8

ALIGN = "mafft"
ALIGN = "indelible"


DISTANCES_FILE = "/groups/itay_mayrose/nomihadar/simulations/subtrees_of_simulated_seqs/subtrees_a_branches_multi_by_2/distances/{align}/true_subtree_{i}_vs_sim_subtree_{j}.csv"


def read_distances(file):

	content = genfromtxt(file, delimiter=',') 
	data = content[1:NUM_SIMULATIONS,:] 
	
	#robinson distance
	rf_distance = data[:,1]

	#symmetric difference distance
	sym_distance = data[:,2]
	
	return (rf_distance, sym_distance)
	
def calc_ttest(a,b):
	t, p = ttest_rel(a, b)
	return (t,p)

def write_logfile():

	with open('logfile_ttest' + output, 'w') as f:
		f.write("distance files:\n")
		f.write(DISTANCES_FILE.format(align = ALIGN,i="i",j="j") + "\n")
	
def main():

	with open("ttest output.csv", 'w') as fout:
	
		fout.write(",".join(["file1", "file2", "RF", "","", "symmetric distance"]) )
		fout.write("\n")
		fout.write(",".join(["", "", "t", "p", "significant", "t", "p", "significant"]))
		fout.write("\n")
	
		for k in  range(1,NUM_RANKS):
			for i in range(k,NUM_RANKS+1):
				for j in range(i+1,NUM_RANKS+1):
				
					file1 = DISTANCES_FILE.format(i=k, j=i, align=ALIGN)
					file2 = DISTANCES_FILE.format(i=k, j=j, align=ALIGN)
					
					data1 = read_distances(file1)
					data2 = read_distances(file2)
				
					t_rf, p_rf = calc_ttest(data1[0],data2[0])
					t_sym, p_sym = calc_ttest(data1[1],data2[1])
					
					significant_rf = True if p_rf < 0.05 else False
					significant_sym = True if p_sym < 0.05 else False
					
					row = "{},{},{},{},{},{},{},{}"\
							.format("{}_{}".format(k,i), "{}_{}".format(k,j), 
									t_rf, p_rf, significant_rf,
									t_sym, p_sym, significant_sym)
					fout.write(row + "\n")

if __name__ == "__main__":

	if len(sys.argv) < 1:
		print "please insert arguments"
		sys.exit(0)
	
	main()
	write_logfile()
	
	
'''
	np.savetxt('t_values.csv', t_values, delimiter=",")
	np.savetxt('p_values.csv', p_values, delimiter=",")
	
	with open("ttest output.csv", 'w') as fout:
		
		fout.write(",".join(["file1", "file2", "RF", "", "symmetric distance"]) )
		fout.write("\n")
		fout.write(",".join(["", "", "t", "p", "t", "p"]))
		fout.write("\n")
		
		for i, file1 in enumerate(files):
			for file2 in files[i+1:]:
				data1 = read_distances(file1)
				data2 = read_distances(file2)
				
				t_rf, p_rf = calc_ttest(data1[0],data2[0])
				t_sym, p_sym = calc_ttest(data1[1],data2[1])
				
				fout.write("{},{},{},{},{},{}".format(os.path.basename(file1), 
														os.path.basename(file2), 
														t_rf, p_rf, 
														t_sym, p_sym) + "\n")

	'''
	