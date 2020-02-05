import os, sys
import time, re
import argparse, logging
import numpy as np
import pandas as pd
from Bio import SeqIO
from subprocess import call
import argparse

sys.path.append("/groups/itay_mayrose/nomihadar/code/")

import mylogger
import run_job as rj
from alignments import compute_statistics as cs

#commands
CMD_INDELIBLE = 'python /groups/itay_mayrose/nomihadar/code/indelible/run_indelible.py -g {gene} -m {model_file} -t {tree_file} -i {indel_file} -n {num_simulations} -max {max_gaps}'

OUTPUT = "chosen_indels.csv"
OUTPUT2 = "fit_indel_parameters_summary.csv"
DIR = "OUTPUT_TEMP"

SUFFIX = ".phy"

ERROR = 'Error'
SIMULATIONS_STATS = "simulated_msas_statistics.csv"
RELATIVE_ERROR = "relative_errors.csv"

INDEL_PARAM = "indel_file.csv"
STAT1 = 'MSA length'
STAT2 = 'average number of gaps'

def create_list(root, suffix):
	paths = []
	#for each alignment of a gene
	for file in os.listdir(root):
		if file.endswith(suffix):
			full_path = os.path.join(root,file)
			paths.append(full_path)
	return paths 					

def relative_error(reference, simulations):	
	d = abs(reference - simulations)
	d = d.div(reference).sum(axis=1)
	return d
	
def run_randomal_indel_params(gene, model_file, tree_file, max_gaps, 
								num_simulations, combs_file, ref_align):
	
	reference_stats = cs.compute_statistics(ref_align)
	reference_stats = reference_stats[[STAT1, STAT2]]
	
	combs = pd.read_csv(combs_file, index_col=0)
	
	os.makedirs("TEMP")
	os.chdir("TEMP")
	
	errors = []
	for index, row in combs.iterrows():
		
		indel_file = combs.loc[[index]]
		indel_file.to_csv(INDEL_PARAM, sep=',')
		
		#run indelible and compute statistics
		cmd = CMD_INDELIBLE.format(gene = gene, model_file = model_file,
									tree_file = tree_file, indel_file = INDEL_PARAM,
									num_simulations = num_simulations,
									max_gaps = max_gaps)
		call(cmd.split(" "))
		
		#compute statistics
		paths = create_list(os.getcwd(), SUFFIX)					
		(stats_df, stats_means_df) = cs.many_alignments(paths)
		stats_df = stats_df[[STAT1, STAT2]]
		
		stats_df.to_csv("../statistics_of_combination_{}.csv".format(index))
		
		#compute relative error
		reference = pd.concat([reference_stats]*stats_df.shape[0])
		reference = reference.reset_index(drop=True)
		stats_df = stats_df.reset_index(drop=True)
		simulations_errors = relative_error(reference, stats_df)
		
		errors.append(simulations_errors.mean())
	
		cmd = "rm -rf *"								
		call(cmd.split(" "))
	
	os.chdir("../")
	
	cmd = "rm -rf TEMP"								
	call(cmd.split(" "))
	
	errors = pd.DataFrame({ERROR : errors}, index=list(combs.index.values))
	errors = pd.concat([combs, errors], axis=1)
	errors.to_csv(RELATIVE_ERROR, index=True)
	
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
	parser.add_argument('-max_gaps', '-max', required=False, default = 50,
						help='max gaps for indelible control file')
	parser.add_argument('-combs_file', required=True,
						help='combinations file')
	parser.add_argument('-ref', required=True,
						help='reference alignment')
	args = parser.parse_args()

	run_randomal_indel_params(args.gene, args.model_file, args.tree_file, 
							args.max_gaps, args.n, args.combs_file, args.ref)
		
	