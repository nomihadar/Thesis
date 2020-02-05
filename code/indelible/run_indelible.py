import os, sys
import time
import re
import argparse
import pandas as pd
from subprocess import call
import numpy as np
sys.path.append("/groups/itay_mayrose/nomihadar/code/")

from trees import rescale_branches as rb
import run_job

INDELIBLE_CMD = '/groups/itay_mayrose/nomihadar/softwares/indelible/myindelible {control_file}' #with my outputs of s lengths
INDELIBLE_CMD = '/groups/pupko/haim/Programs/indelible/INDELibleV1.03/src/indelible {control_file}'

FLAG = "INDELIBLE_END"

MAX_GAPS_LENGTH = 50

#[output]          	FASTA
#[fastaextension]	fasta


CONTROL_FILE = """
[TYPE] NUCLEOTIDE 1

[SETTINGS]
	[phylipextension] 	phy
	[output]          	PHYLIP
	[fileperrep]      	TRUE
	[printrates] 		TRUE    

[MODEL] mymodelname
	[submodel] GTR {CT} {AT} {GT} {AC} {CG} 
	[indelmodel] POW {A} {max_gaps_length}
	[indelrate] {IR}
	[rates] 0 {GAMMA} 16      
	[statefreq] {fT} {fC} {fA} {fG}

[TREE] mytree {tree} 

[PARTITIONS] partitionname 
	[mytree mymodelname {root_length}]

[EVOLVE] partitionname {num_simulations} {output}
"""
# //USER {mylengthmodel} 

# GTR: a={CT} b={AT} c={GT} d={AC} e={CG} (f={AG})

# rate A <-> C: ...  rate d
# rate A <-> G: ...  rate f
# rate A <-> T: ...  rate b
# rate C <-> G: ...  rate e
# rate C <-> T: ...  rate a
# rate G <-> T: ...  rate c


def run_indelible(gene):

	indelible_cmd = INDELIBLE_CMD.format(gene = gene, 
										control_file = "control.txt")								
	#run_job.run_job(indelible_cmd, "job_indelible.sh")
	call(indelible_cmd.split(" "))
	
def get_indel_params(indel_file, gene):
	'''
	df = pd.read_csv(indel_file,index_col='gene')
	a = df.loc[gene]['a']
	ir = df.loc[gene]['ir']
	rl = df.loc[gene]['rl']
	'''
	
	indels = pd.read_csv(indel_file, header=0)
	rl = int(indels['rl'][0])
	a = indels['a'][0]
	ir = indels['ir'][0]
	
	parameters = (rl, a, ir)
	return 	parameters

def get_model_parameters(gene, model_file):
	
	with open(model_file, 'r') as f:
		model_file = f.read().splitlines() 
		
		if len(model_file) < 20:
			parameters = model_file[3:18]
		else:
			for i, line in enumerate(model_file):
				if gene in line:
					parameters = model_file[i:i+14]
					break
	
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
		
def fix_tree_branches(tree_path):

	#get the tree for the control file
	with open(tree_path, 'r') as f:
		tree = f.read().splitlines()[0]
	fixed_tree = rb.rescale_branches(tree)
	
	return fixed_tree
	
def create_control_file(gene, model_parameters, tree, indel_parameters, 
						num_simulations, max_gaps_length):
	
	(alpha, rates, frequencies) = model_parameters
	(rl, a, ir) = indel_parameters
	
	#create the control file 
	control_file = CONTROL_FILE.format(CT = rates['CT'],
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
									tree = tree,
									root_length = rl,
									max_gaps_length = max_gaps_length,
									num_simulations = num_simulations,
									output = gene)

	with open('control.txt', 'w') as fout:
		fout.write(control_file)	
		
		
def create_control_file2(gene, model_parameters, tree, indel_parameters, 
						num_simulations, lengthmodel):
	
	(alpha, rates, frequencies) = model_parameters
	(rl, a, ir) = indel_parameters
	
	#create the control file 
	control_file = CONTROL_FILE.format(CT = rates['CT'],
									AT = rates['AT'],
									GT = rates['GT'],
									AC = rates['AC'],  
									CG = rates['CG'],
									IR = "{:.10f}".format(ir),
									GAMMA = "{:.10f}".format(alpha),
									fT = frequencies['T'],
									fC = frequencies['C'],
									fA = frequencies['A'],
									fG = frequencies['G'],
									tree = tree,
									root_length = rl,
									mylengthmodel = lengthmodel,
									num_simulations = num_simulations,
									output = gene)

	with open('control.txt', 'w') as fout:
		fout.write(control_file)	
	
	
def f(files):
	with open(files, 'r') as f:
		paths = f.read().splitlines()
	
	observations = []
	for path in paths:
		obs = np.loadtxt(path, 'int', ndmin=1)
		observations.extend(obs)
					
	return max(observations)
	
def main(gene, model_file, tree_file, indel_file, 
		num_simulations, lengthmodel='', max_gaps_length=MAX_GAPS_LENGTH):

	#read tree
	tree = fix_tree_branches(tree_file)
	
	#get the model parameters
	model_parameters = get_model_parameters(gene, model_file)

	#get the indel parameters 
	indel_parameters = get_indel_params(indel_file, gene)
	
	#max_gaps_length = f(max_gaps_length)
	
	#create control file 
	if not lengthmodel:
		create_control_file(gene, model_parameters, tree, indel_parameters,
							num_simulations, max_gaps_length)
	else:
		create_control_file2(gene, model_parameters, tree, indel_parameters,
							num_simulations,lengthmodel)					
		
	#run indelible
	indelible_cmd = INDELIBLE_CMD.format(control_file = "control.txt")
	call(indelible_cmd.split())
	
	#create a flag file
	open(FLAG, 'w').close()
	

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
	parser.add_argument('--max_gaps', '-max', required=False, type=int,
						default=50,help='max length of gaps')
						
	parser.add_argument('--mylengthmodel', '-lengthmodel', required=False,
						help='file with my length model')
						
	args = parser.parse_args()
	
	main(args.gene, args.model_file, args.tree_file, 
		args.indel_file, args.num_simulations, args.mylengthmodel, args.max_gaps)	
		
		