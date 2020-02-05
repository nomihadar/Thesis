import sys, os
import numpy as np
import scipy.stats as stats
from numpy import genfromtxt

NUM_SIMULATIONS = 31
NUM_RANKS = 8

ALIGN = "mafft"
ALIGN = "indelible"


DISTANCES_FILE = "/groups/itay_mayrose/nomihadar/simulations/subtrees_of_simulated_seqs/subtrees_a_branches_multi_by_2/distances/{align}/true_subtree_{i}_vs_sim_subtree_{j}.csv"

def write_logfile():
	with open('logfile_anova' + output, 'w') as f:
		f.write("distance files:\n")
		f.write(DISTANCES_FILE.format(align = ALIGN,i="i",j="j") + "\n")
		
def read_distances(file):

	content = genfromtxt(file, delimiter=',') 
	data = content[1:NUM_SIMULATIONS,:] 
	
	#robinson distance
	rf_distance = data[:,1]

	#symmetric difference distance
	sym_distance = data[:,2]
	
	return (rf_distance, sym_distance)
	
def calc_anova(groups):
	#print groups
	f, p = stats.f_oneway(*groups)
	return (f,p)

def main():

	with open("anova output.csv", 'w') as fout:
	
		fout.write(",".join(["true tree", "RF", "","", "symmetric distance"]) )
		fout.write("\n")
		fout.write(",".join(["", "f", "p", "significant", "f", "p", "significant"]))
		fout.write("\n")
	
		for k in  range(1,NUM_RANKS):
			
			rf_distances = []
			sym_distances = []
			for i in range(k,NUM_RANKS+1):
				file = DISTANCES_FILE.format(i=k, j=i, align=ALIGN)
				
				(rf_distance, sym_distance) = read_distances(file)
				rf_distances.append(rf_distance)
				sym_distances.append(sym_distance)
				
			f_rf, p_rf = calc_anova(rf_distances)
			f_sym, p_sym = calc_anova(sym_distances)
			
			significant_rf = True if p_rf < 0.05 else False
			significant_sym = True if p_sym < 0.05 else False
				
			row = "{},{},{},{},{},{},{}"\
					.format(k, f_rf, p_rf, significant_rf,
							f_sym, p_sym, significant_sym)
			fout.write(row + "\n")
			
if __name__ == "__main__":

	if len(sys.argv) < 1:
		print "please insert arguments"
		sys.exit(0)
	
	main()
	write_logfile()
	
	