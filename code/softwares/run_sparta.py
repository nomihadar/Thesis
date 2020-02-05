import os, sys
import time
import re
import argparse
import pandas as pd
from subprocess import call

sys.path.append("/groups/itay_mayrose/nomihadar/code/")

from trees import rescale_branches as rb
import run_job

SPARTA_PATH = "/groups/itay_mayrose/nomihadar/softwares/sparta_V20150910/code/sparta"
SPARTA_CMD = SPARTA_PATH + ' {control_file} {alignment} {output_path} {num_iterations}'
TEMPLATE_CONTROL = 'template_control.txt'

MAX_GAPS_LENGTH = 50

CONTROL_FILE = '''
[TYPE] NUCLEOTIDE 2	
[SETTINGS]
	[output] FASTA
	[fileperrep] TRUE 
[MODEL]    modelname       
  [submodel]  HKY 2.5                	
  [statefreq] 0.25 0.25 0.25 0.25
  [indelmodel]  POW  1.3 50 
  [indelrate]   0.02

[TREE] treename 
{tree}

[PARTITIONS]   partitionname           
  [treename modelname  350]
 
[EVOLVE] partitionname 1 try
'''

def run_sparta(alignment, num_iterations):
	sparta_cmd = SPARTA_CMD.format(alignment = alignment, 
									control_file = TEMPLATE_CONTROL,
									num_iterations = num_iterations,
									output_path = ".")								
	run_job.run_job(sparta_cmd, "job_sparta.sh")

def fix_tree_branches(tree_path):

	#get the tree for the control file
	with open(tree_path, 'r') as f:
		tree = f.read().splitlines()[0]
	fixed_tree = rb.rescale_branches(tree)
	
	return fixed_tree
	
def create_control_file(tree):
	#create the control file 
	control_file = CONTROL_FILE.format(tree = tree)
	with open(TEMPLATE_CONTROL, 'w') as fout:
		fout.write(control_file)	
	
def main(tree_file, alignment, num_iterations):

	#read tree
	tree = fix_tree_branches(tree_file)
	
	#create control file 
	create_control_file(tree)
						
	run_sparta(alignment, num_iterations)

if __name__ == "__main__":

	parser = argparse.ArgumentParser()	
	parser.add_argument('--tree_file', '-t', required=True,
						 help='path to tree')
	parser.add_argument('--msa', '-a', required=True,
						help='refernce FASTA alignment')					 
	parser.add_argument('--num_iterations', '-n', required=True,
						help='number of iterations')				
	args = parser.parse_args()
	
	main(args.tree_file, args.msa, args.num_iterations)	
		
		