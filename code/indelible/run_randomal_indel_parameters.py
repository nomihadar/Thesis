import os, sys
import argparse
import pandas as pd
import numpy as np
from Bio import SeqIO 

sys.path.append("/groups/itay_mayrose/nomihadar/code/")

import create_paths_list as ls
from indelible import run_indelible
from alignments import get_alignment_length as al

OUTPUT = "{}_indel_combinations.csv"
				
IR_VALUES = [0.000001, 0.00001, 0.0001, 0.0001, 0.001,
			0.000002, 0.00002, 0.0002, 0.0002, 0.002,
			0.000004, 0.00004, 0.0004, 0.0004, 0.004,
			0.000008, 0.00008, 0.0008, 0.0008, 0.008] 

A_VALUES = [1.00000001, 1.0000001, 1.000001, 1.00001, 1.0001, 
			1.001, 1.01, 1.000005, 1.00005, 1.0005, 1.005, 
			1.05, 1.1, 1.15, 1.2, 1.25, 1.3, 1.35, 1.4, 1.5]	
			
DIR = "aligments_statistics"
SUFFIX = ".phy"
SIMULATIONS_STATS = "simulated_msas_statistics.csv"
COMPUTE_STATS_CMD = "python ~/code/alignments/compute_statistics.py -f {paths} -paths -o {output}"
PATHS_FILE = "paths.ls"

CMD_INDELIBLE = 'python ~/code/indelible/run_indelible.py -g {gene} -m {model_file} -t {tree_file} -i {indel_file} -n {num_simulations} -max {max_gaps}'
CMD_LIST = 'python ~/code/create_paths_list.py -r {root_dir} -s {suffix} -o {output}'


FLAG = "INDELIBLE_ENDS_OK"

def compute_statistics(root, num_simulations):

	os.makedirs(DIR)
	os.chdir(DIR)
	
	paths = ls.main(".", SUFFIX)
	
	#compute statistics
	cmd = COMPUTE_STATS_CMD.format(alignment = PATHS_FILE, 
									output = SIMULATIONS_STATS)
	rj.run_job(cmd, "job_compute_statistics.sh")
			
	os.chdir("../")
		
def create_indel_file(gene, a_value, ir, rl):

	#create indel file
	indel_params = {'a': [a_value], 'ir': [ir], 'rl': [rl]}
	
	#outputfile
	df = pd.DataFrame(indel_params)
	indel_file = "indel_file.csv"
	df.to_csv(indel_file, sep=',', index=False)
	
	return indel_file
	
def main(gene, model_file, tree_file, ref_align, num_simulations):

	comb_id = 1 #combination id 
	combinations = {"#id": [], "rl": [], "ir": [], "a": []}
	
	for ir in IR_VALUES:
		for a in A_VALUES:
					
			#run indelible with those parameters
			dir_name = "{}_comb_{}".format(gene, comb_id)
			os.makedirs(dir_name)
			os.chdir(dir_name)
			
			rl = int(al.get_average_seqs_length(ref_align))
			indel_file = create_indel_file(gene, a, ir, rl)
			
			#run indelible and compute statistics
			cmd = CMD_INDELIBLE.format(gene = gene, model_file = model_file,
										tree_file = tree_file, indel_file = indel_file,
										num_simulations = num_simulations,
										max_gaps = max_gaps)
				
			#cmd += "\nmkdir statistics\ncd statistics\n"

			cmd += "\n" + CMD_LIST.format(root_dir = ".",
									suffix = SUFFIX)			
				
			cmd += "\n" + COMPUTE_STATS_CMD.format(paths = PATHS_FILE, 
											output = SIMULATIONS_STATS)
											
			cmd += "\n" + "rm -rf *.phy *.fas"								
			
			rj.run_job(cmd, "job_indelible_and_statistics.sh")
			
			#compute statistics
			compute_statistics()
								
			os.chdir("../")
			
			combinations["#id"].append(comb_id) 
			combinations["rl"].append(rl) 
			combinations["a"].append(a) 
			combinations["ir"].append(ir) 
		
			comb_id += 1
			
	df = pd.DataFrame(combinations)
	output = OUTPUT.format(gene) 
	df.to_csv(output, sep=',', index=False)
	
if __name__ == "__main__":

	args = parser.parse_args()
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--gene', '-gene', required=True,
						help='name of gene')
	parser.add_argument('--model_file', '-m', required=True,
						help='file of model (output of examl)')
	parser.add_argument('--tree_file', '-t', required=True,
						 help='path to tree')
	parser.add_argument('--num_simulations', '-n', required=True,
						help='number of simulations')
	parser.add_argument('--ref_align', '-r', required=True,
						help='refernce alignment')
	args = parser.parse_args()
	
	main(args.gene, args.model_file, args.tree_file, 
		args.ref_align, args.num_simulations)
	
	