import sys, os, time, re, argparse, logging
import numpy as np
from ete3 import Tree
import pandas as pd
from subprocess import call

sys.path.append("/groups/itay_mayrose/nomihadar/code/")

import mylogger 
import run_ktreedist
import my_treedist
from run_job import run_job

OUTPUT = "tree_dist_output"

TURE_TREE = "/groups/itay_mayrose/nomihadar/simulations/subtrees_of_true_tree/subtrees_a_1/subtree_{i}.tree"
SIM_TREE = "/groups/itay_mayrose/nomihadar/simulations/subtrees_of_simulated_seqs/subtree_a_1/pruned/{align}/from_subtree_{i}/subtrees_{j}/subtree_{j}_{k}_pruned.tree"

ALIGN = "mafft" #"mafft" #"indelible"

DISTANCE_METHOD = "ktreedist" #"my_treedist"
DISTANCE_CMD = {"ktreedist": "python ~/code/trees/run_ktreedist.py -rt {reference_tree} -ct {comparison_tree} -o {output_name}",
				"my_treedist": "python ~/code/trees/my_treedist.py {tree1} {tree2}"}
TEMP_DIR = "{}-{}_{}"	
DISTANCE_OUTPUT = "{}-{}_{}.distance_output.csv"		

def compute_distance(tree1, tree2, output_name):

	cmd = DISTANCE_CMD[DISTANCE_METHOD].format(reference_tree = tree1,
												comparison_tree = tree2,
												output_name = output_name)
	run_job(cmd, "job_compute_distance.sh")
	
def create_distances_jobs(ranks, simulations):		
	
	for i in range(1,ranks+1):
	
		tree1_path = TURE_TREE.format(i=i)
		
		for j in range(i,ranks+1):	
			output_name = "true_{i}_vs_simulated_{j}".format(i=i,j=j)
	
			for k in range(1,simulations+1):
			
				tree2_path = SIM_TREE.format(i=j, j=i, k=k, align = ALIGN) 
				output_distance_file = DISTANCE_OUTPUT.format(i,j,k)
				
				os.mkdir(TEMP_DIR.format(i,j,k))
				os.chdir(TEMP_DIR.format(i,j,k))
				
				#compute distance
				compute_distance(tree1_path, tree2_path, output_distance_file)
				
				os.chdir("../")
	
def collect_outputs(ranks, simulations):
	
	df_all_means = pd.DataFrame(index=range(1,ranks+1), columns=range(1,ranks+1))
	df_all_means.fillna(' ')

	df_all_std = pd.DataFrame(index=range(1,ranks+1), columns=range(1,ranks+1))
	df_all_std.fillna(' ')
	
	for i in range(1,ranks+1):
		for j in range(i,ranks+1):	
			distances = []
			for k in range(1,simulations+1):
				
				#read distance from distance file
				
				os.chdir(TEMP_DIR.format(i,j,k))
				
				distance_file = DISTANCE_OUTPUT.format(i,j,k)
				while not os.path.isfile(distance_file):
					#print distance_file
					time.sleep(5)
				
				df = pd.read_csv(distance_file)
				distances.append(df['distance'][0])
				
				os.chdir("../")
			
			mean = np.mean(distances)
			std = np.std(distances)
			'''
			stats = [mean, median, var]
			stats_names = ["mean", "median", "variance"]
			'''
			#create dataframe
			d = {"simulation id": range(1,simulations+1), 
				"distance": distances}
			df = pd.DataFrame(d)
			
			#outputfile
			cols = df.columns.tolist()
			df = df[cols[-1:] + cols[:-1]]
			output_name = "true_{i}_vs_simulated_{j}.csv".format(i=i,j=j)
			df.to_csv(output_name, sep=',', index=False)
			
			#log file
			tree1_path = TURE_TREE.format(i=i)
			trees2_path = SIM_TREE.format(i=j, j=i, k='k', align = ALIGN)
			logging.info("compare {} VS {}".format(tree1_path, trees2_path))
			
			df_all_means[j][i] = mean
			df_all_std[j][i] = std
			
	df_all_means.to_csv("summary_means.csv", sep=',', index=True)
	df_all_std.to_csv("summary_std.csv_std", sep=',', index=True)

def main(ranks, simulations):
	
	create_distances_jobs(ranks, simulations)
	time.sleep(5)
	collect_outputs(ranks, simulations)

	#call(["rm", "-rf", "*temp*"])
	
if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='')
	
	parser.add_argument('--ranks', '-r', required=True,
						help='number of ranks in tree')
	
	parser.add_argument('--simulations', '-n', required=True,
						help='number of simulations')			

	args = parser.parse_args()
	num_ranks = int(args.ranks)
	num_simulations = int(args.simulations)
	
	mylogger.initialize("trees_distances.logfile")
	
	logging.info("num ranks: {}".format(num_ranks))
	logging.info("number of simulations: {}".format(num_simulations))
	logging.info("paths of true trees: {}".format(TURE_TREE))
	logging.info("paths of simulated trees: {}".format(SIM_TREE))
	logging.info("alignments aligned by: {}".format(ALIGN))
	logging.info("distance method: {}".format(DISTANCE_METHOD))

	main(num_ranks, num_simulations)
