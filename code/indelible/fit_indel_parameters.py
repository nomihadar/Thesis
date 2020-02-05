import os, sys
import time, re
import argparse, logging
import numpy as np
import pandas as pd
from Bio import SeqIO
from subprocess import call
import argparse
from itertools import product

sys.path.append("/groups/itay_mayrose/nomihadar/code/")

import mylogger
import run_job as rj
from alignments import compute_statistics as cs

#commands
CMD_HELPER = 'python /groups/itay_mayrose/nomihadar/code/indelible/fit_indel_parameters_helper.py -g {gene} -m {model_file} -t {tree_file} -combs_file {combs_file} -n {num_simulations} -max {max_gaps} -ref {ref_align}'
		
OUTPUT = "chosen_indels.csv"
OUTPUT2 = "fit_indel_parameters_summary.csv"

DIR_TEMP = "TEMP"
DIR = "SPLIT_{}"

ERROR = 'Error'
RELATIVE_ERROR = "relative_errors.csv"

STAT3 = 'average length of sequences'

INTERVALS = 30
SPLIT_SIZE = 30

IR_VALUES = np.logspace(-6, -2, INTERVALS, endpoint=True)
A_VALUES = np.logspace(np.log10(0.00000001), np.log10(0.6), INTERVALS, endpoint=True) + 1

def create_list(root, suffix):
	paths = []
	#for each alignment of a gene
	for root, dirs, files in os.walk(root, topdown=True):
		for file in files:
			if file.endswith(suffix):
				full_path = os.path.join(root,file)
				paths.append(full_path)
	return paths 					
			
def choose_indels(output):

	paths = []
	
	while len(paths) < SPLIT_SIZE:
		paths = create_list(DIR_TEMP, RELATIVE_ERROR)
		logging.info("paths size:,{}".format(len(paths)))
		time.sleep(60)
		
	#concatenate statistics
	frames = []
	for path in paths:
		df = pd.read_csv(path, index_col=0)
		frames.append(df)
	
	final = pd.concat(frames)
	final = final.sort_values([ERROR])
	final.to_csv(OUTPUT2)
	
	#write chosen indels 
	chosen_indels = final.iloc[0:1,:]
	chosen_indels.to_csv(output, index=True)
	
def remove_folder(path):
	cmd = "rm -rf {}".format(path)
	call(cmd.split(" "))
	
def run_randomal_indel_params(gene, model_file, tree_file,  
								max_gaps, num_simulations, ref_align):
	
	statistics = []
	
		#compute statistics of reference (real) alignment 
	reference_stats = cs.compute_statistics(ref_align)
	combs = pd.DataFrame(list(product(IR_VALUES, A_VALUES)), columns=['ir', 'a'])
	combs['rl'] =  int(reference_stats[STAT3][0])
	
	combs_dfs = np.array_split(combs, SPLIT_SIZE)

	os.makedirs(DIR_TEMP)
	os.chdir(DIR_TEMP)
	
	for i, comb in enumerate(combs_dfs):
		
		dir = DIR.format(i)
		os.makedirs(dir)
		os.chdir(dir)
	
		comb_file = os.path.join(os.getcwd(),"comb_{}.csv".format(i+1))
		comb.to_csv(comb_file, index=True)
		
		cmd = CMD_HELPER.format(gene = gene, 
								model_file = model_file,
								tree_file = tree_file, 
								combs_file = comb_file,
								num_simulations = num_simulations,
								max_gaps = max_gaps,
								ref_align = ref_align)
		rj.run_job(cmd, "job.sh")
		
		os.chdir("../")
		
	os.chdir("../")

	
def main(gene, model_file, tree_file, num_simulations, 
		ref_align, max_gaps, output):
	
	root = os.getcwd()
	
	#run random indel parameters and compute statistics of simulated alignments
	#run_randomal_indel_params(gene, model_file, tree_file,
	#						max_gaps, num_simulations, ref_align)
	
	#collect data compute and output chosen indels 
	choose_indels(output)
	
	logging.info("ENDS OK")
	
def main_paths(gene, model_file, tree_file, num_simulations, 
		paths_file, max_gaps, output):
	
	root = os.getcwd()
	
	with open(paths_file, 'r') as f:
		msa_files = f.read().splitlines()
		
	for ref_align in msa_files:
	
		dir = os.path.basename(ref_align)
		os.makedirs(dir)
		os.chdir(dir)
		
		main(gene, model_file, tree_file, num_simulations, 
			ref_align, max_gaps, output)
		
		os.chdir("../")
		
if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument('--gene', '-g', required=True,
						help='name of gene')
	parser.add_argument('--model_file', '-m', required=True,
						help='file of model (output of examl)')
	parser.add_argument('--tree_file', '-t', required=True,
						 help='path to tree')
	parser.add_argument('-n', required=True, type=int,
						help='number of simulations')
	parser.add_argument('-ref', '-r', required=True,
						help='reference alignment')
	parser.add_argument('-max_gaps', '-max', required=False, default = 50,
						help='max gaps for indelible control file')
	parser.add_argument('-output', '-o', required=False, default = OUTPUT,
						help='output name of final file')
	parser.add_argument('-paths', action='store_true', 
						help='file contains paths')						
	args = parser.parse_args()
	
	mylogger.initialize("fit_indel_parameters_logfile.csv")
	logging.info("gene name:,{}".format(args.gene))
	logging.info("model file:,{}".format(args.model_file))
	logging.info("tree file:,{}".format(args.tree_file))
	logging.info("num simulations:,{}".format(args.n))
	logging.info("reference alignment:,{}".format(args.ref))
	logging.info("max gaps length:,{}".format(args.ref))
	logging.info("range divided to: {}".format(INTERVALS))
	
	if args.paths:
		main_paths(args.gene, args.model_file, args.tree_file, 
			args.n, args.ref, args.max_gaps, args.output)
	else:
		main(args.gene, args.model_file, args.tree_file, 
			args.n, args.ref, args.max_gaps, args.output)
		
	