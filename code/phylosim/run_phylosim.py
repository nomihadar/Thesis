import os, sys
import time
import re
import argparse
import pandas as pd
from subprocess import call

sys.path.append("/groups/itay_mayrose/nomihadar/code/")

import run_job

R_CMD = 'module load R/R342\nR CMD BATCH --no-save --no-restore {r_file} r_out_file.txt'
MAX_GAPS_LENGTH = 50
R_FILE = 'phylosim.R'

FLAG = "ENDS_OK"

PHYLOSIM_CODE = """
library("phylosim")
library("poweRlaw")

TREE_FILE = "{tree_file}"

rates = list(a = {CT}, b = {AT}, c = {GT}, 
             d = {AC}, e = {CG}, f = 1)
bases = c({fT}, {fC}, {fA}, {fG})
sub_process = GTR(rate.params = rates, base.freqs = bases)

tolerance_probs_table = read.table("{tolerance_file}")
tolerance_probs = tolerance_probs_table[[1]]
rl = length(tolerance_probs)

root_seq = NucleotideSequence(length=rl)
length_dis = expression(rplcon(1, 1,{A})) 

del_process = ContinuousDeletor(rate={IR},dist=length_dis, 
								max.length={max_gaps_length})

insert_process = ContinuousInsertor(rate={IR}, dist=length_dis,
									max.length={max_gaps_length})

attachProcess(root_seq,sub_process)
attachProcess(root_seq,del_process)
attachProcess(root_seq,insert_process)

plusInvGamma(root_seq, sub_process, pinv = 0, shape = {GAMMA}, ncat = 16)

setDeletionTolerance(root_seq, del_process, tolerance_probs, 1:root_seq$length)

template = NucleotideSequence(length=10)
attachProcess(template,sub_process)
insert_process$writeProtected = FALSE
insert_process$templateSeq = template

sampleStates(root_seq)
sim = PhyloSim(root.seq = root_seq, phylo = read.tree(TREE_FILE));
Simulate(sim)
saveAlignment(sim,file="{gene}_phylosim.fas", skip.internal = TRUE)
"""

def run_R():

	#run R
	r_cmd = R_CMD.format(r_file = R_FILE)
	run_job.run_job(r_cmd, "job_R_phylosim.sh")
	
def get_indel_params(indel_file):
	indels = pd.read_csv(indel_file, header=0)
	rl = int(indels['rl'][0])
	a = indels['a'][0]
	ir = indels['ir'][0]
	parameters = (rl, a, ir)
	return 	parameters

def get_model_parameters(gene, model_file):
	
	with open(model_file, 'r') as f:
		model_file = f.read().splitlines() 
		
		for i, line in enumerate(model_file):
			if gene in line:
				parameters = model_file[i:i+14]
	
	rates = {}
	frequencies = {}
	for line in parameters:
		
		regex = re.search("alpha: (\d+\.\d+)", line)
		if regex:
			alpha = float(regex.group(1))
			
		regex = re.search("rate ([ACGT]) <-> ([ACGT]): (\d+\.\d+)", line)
		if regex:
			nucleotides = regex.group(1) + regex.group(2)
			rate = float(regex.group(3))
			rates[nucleotides] = rate
			
		regex = re.search("freq pi\(([ACGT])\): (\d+\.\d+)", line)
		if regex:
			nucleotide = regex.group(1)
			frequency = float(regex.group(2))
			frequencies[nucleotide] = frequency
	
	return (alpha, rates, frequencies)
		
	
def create_code_file(gene, model_parameters, tree, indel_parameters, 
						num_simulations, max_gaps_length, tolerance_probs):
	
	(alpha, rates, frequencies) = model_parameters
	(rl, a, ir) = indel_parameters
	
	#create the control file 
	r_code = PHYLOSIM_CODE.format(CT = rates['CT'],
								AT = rates['AT'],
								GT = rates['GT'],
								AC = rates['AC'],  
								CG = rates['CG'],
								A = "{:.10f}".format(a),
								IR = "{:.10f}".format(ir),
								GAMMA = "{:.10f}".format(alpha),
								fT = frequencies['T'],
								fC = frequencies['C'],
								fA = frequencies['A'],
								fG = frequencies['G'],
								tree_file = tree,
								root_length = rl,
								max_gaps_length = max_gaps_length,
								tolerance_file = tolerance_probs,
								gene = gene)

	with open(R_FILE, 'w') as fout:
		fout.write(r_code)	
	
def main(gene, model_file, tree_file, indel_file, 
		num_simulations, tolerance_probs, max_gaps_length=MAX_GAPS_LENGTH):
	
	#get the model parameters
	model_parameters = get_model_parameters(gene, model_file)

	#get the indel parameters 
	indel_parameters = get_indel_params(indel_file)
	
	#create control file 
	create_code_file(gene, model_parameters, tree_file, indel_parameters,
					num_simulations, max_gaps_length, tolerance_probs)
	
	while not os.path.isfile(R_FILE):
		time.sleep(1)
	
	run_R()
	#create a flag file
	#open(FLAG, 'w').close()
	

if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument('--gene', '-g', required=True,
						help='name of gene')
	parser.add_argument('--model_file', '-m', required=True,
						help='file of model (output of examl)')					
	parser.add_argument('--tree_file', '-t', required=True,
						 help='path to tree')
	parser.add_argument('--num_simulations', '-n', required=True,
						help='number of simulations')				
	parser.add_argument('--indel_file', '-i', required=True,
						help='path to file contains indel parameters')
	parser.add_argument('--max_gaps', '-max', required=True, type=int,
						help='max length of gaps')
	parser.add_argument('-tolerance_probs', required=True, 
						help='files with tolerance probabilities for each root site')
	args = parser.parse_args()
	
	main(args.gene, args.model_file, args.tree_file, 
		args.indel_file, args.num_simulations, args.tolerance_probs, args.max_gaps)	
		
		