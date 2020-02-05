import sys
import os
from subprocess import call
from ete3 import Tree
from sample_tree import *

#msa must be in PHYLIP format 

PHYML_QSUB = """#!/bin/tcsh

#$ -N phyML_ITS
#$ -S /bin/tcsh
#$ -cwd
#$ -l itaym
#$ -e $JOB_NAME.$JOB_ID.ER
#$ -o $JOB_NAME.$JOB_ID.OU

/share/apps/bin/PhyML -u {tree_path} -i {msa_path} -m GTR -a e -o r --quiet
\n
"""

def run_phyML(tree_path, k):

	#create qsub file 
	qsub_file = "qsub_pda.sh"
	with open(qsub_file, 'w') as fout:
		qsub_args = PHYML_QSUB.format(tree_path = tree_path, 
									msa_path = msa_path, k = k)
		fout.write(qsub_args)
	
	#run pda on queue
	qsub_cmd = "qsub {}".format(qsub_file)
	call(qsub_cmd.split(" "))	

def get_tree_length(tree_path):
	input_tree = Tree(tree_path)
	return len(input_tree)
	

def get_alignment 
	
def	main(tree_path):
		
	if get_tree_length(tree_path) > 3999:
		
		for sample_id in range(10):
		
			output_dir = "sampl_{sample_id}".format(sample_id = sample_id)
		
			os.makedirs(output_dir)
			os.chdir(output_dir)
			
			#sample tree 
			run_pda(tree_path, 3999)
			
			#get alignment of the sampled tree
			get_alignment()
			
			os.chdir("../")
	
	else:
	
		
	

if __name__ == "__main__":

	if len(sys.argv) < 2:
		print "please insert arguments"
		sys.exit(0)
	
	tree_path = sys.argv[1]
	
	#num species to sample 
	num_to_sample = int(sys.argv[2])
	
	num_species = get_num_species_in_tree(tree_path)
	
	print "num species in tree: ", num_species
	
	run_phyML(tree_path, num_species)
	
	#create_directory(num_species, tree_path)