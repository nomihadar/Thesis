import sys
import os
from subprocess import call
from ete3 import Tree

#k = num to sample 

PDA_QSUB = """#!/bin/tcsh

#$ -N pda_{k}
#$ -S /bin/tcsh
#$ -cwd
#$ -l itaym
#$ -e $JOB_NAME.$JOB_ID.ER
#$ -o $JOB_NAME.$JOB_ID.OU

pda {tree_path} pda_output_{k}_species.nw -k {k}
\n
"""

def run_pda(tree_path, k):

	#create qsub file 
	qsub_file = "qsub_pda.sh"
	with open(qsub_file, 'w') as fout:
		qsub_args = PDA_QSUB.format(tree_path = tree_path, k = k)
		fout.write(qsub_args)
	
	#run pda on queue
	qsub_cmd = "qsub {}".format(qsub_file)
	call(qsub_cmd.split(" "))	

def create_directory(num_species, tree_path):

	for k in range(200, num_species, 200):
		
		run_pda(tree_path, k)
		# output_dir = "{k}_species".format(k = k)
		# if not os.path.exists(output_dir):
			# os.makedirs(output_dir)
			# os.chdir(output_dir)
			
			# os.chdir("../")
	
def get_num_species_in_tree(tree_path):

	input_tree = Tree(tree_path)
	
	return len(input_tree)
	
if __name__ == "__main__":

	if len(sys.argv) < 2:
		print "please insert arguments"
		sys.exit(0)
	
	tree_path = sys.argv[1]
	
	#num species to sample 
	num_to_sample = int(sys.argv[2])
	
	num_species = get_num_species_in_tree(tree_path)
	
	print "num species in tree: ", num_species
	
	run_pda(tree_path, num_to_sample)
	
	#create_directory(num_species, tree_path)