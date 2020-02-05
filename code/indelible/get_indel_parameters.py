import os, sys
import numpy as np
import pandas as pd

sys.path.append("/groups/itay_mayrose/nomihadar/code/")

import run_job as rj
from alignments import get_alignment_length as al

FIT_INDEL_CMD = "python ~/code/indelible/fit_indel_parameters.py -g {gene} -m {model_file} -t {tree_file} -r {reference} -n {num_simulations}"
INDEL_FILE = "chosen_indels.csv"
	
def write(rl, a, ir):
		
	#create indel file
	indel_params = {'a': [a], 'ir': [ir], 
					'rl': [rl]}
	#outputfile
	df = pd.DataFrame(indel_params)	
	df.to_csv(INDEL_FILE, index=False)
	
#methods = constant, distribution, block_optimized
def get_indel_params(gene, model_file, tree_file, indel_file,
					num_simulations, reference, method = "constant"):
	
	if method == "constant":
		
		df = pd.read_csv(indel_file)
		a = df['a'][0]
		ir = df['ir'][0]
		rl = int(al.get_average_seqs_length(reference))
	
		write(rl, a, ir)		
	
	if method == "distribution":

		df = pd.read_csv(indel_file)
		a = df['a'][0]
		ir = df['ir'][0]
		rl = int(al.get_average_seqs_length(reference))
		
		# mean and standard deviation
		while True:
			new_a = np.random.normal(a, a/5)
			if new_a > 1:
				break
		new_ir = np.random.normal(ir, ir/5)
		
		write(rl, new_a, new_ir)	
	
	if method == "block_optimized":
		
		#fit indel parameters
		cmd = FIT_INDEL_CMD.format(gene = gene, 
									model_file = model_file,
									tree_file = tree_file,
									reference = reference,
									num_simulations = num_simulations)
		rj.run_job(cmd, "job_fit_indel_parameters.sh")
		