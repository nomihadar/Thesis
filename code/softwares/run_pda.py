import os, sys
import argparse, re
from subprocess import call
import time
import os.path

sys.path.append("/groups/itay_mayrose/nomihadar/code/")

import run_job
from trees import rescale_branches as rb
from trees import get_tree_species as get_species

'''
#convert branches
	tree_formated = rb.rescale_branches(tree_file)
	with open("adjusted_tree.nw", "w") as f:
		f.write(tree_formated)
		f.write("\n")
	tree_file = "adjusted_tree.nw"
'''

PDA_CMD = 'pda {tree_file} pda_output -k {num_to_sample}\n'
PDA_CMD += 'touch ends_ok'

def extract_tree(filepath):

	#open file and extract the tree:
	with open (filepath, "r") as f:
		content = f.read()
		regex = re.search(r'(\(.*;)', content)
		tree = regex.group(0)
	
	get_species.get_tree_species(tree)		
	
def run_pda(tree_file, k):
	
	cmd = PDA_CMD.format(tree_file=tree_file, num_to_sample=k)
	run_job.run_job(cmd, "job_run_pda.sh")
	
	while not os.path.isfile("ends_ok"):
		time.sleep(5)
	
	extract_tree("pda_output")
	
def run_pda_paths(trees_file, num_to_sample):
	
	#get input list_path
	with open(trees_file, 'r') as f:
		paths = f.read().splitlines()

	for path in paths:
		dir = os.path.basename(path)
		os.makedirs(dir)
		os.chdir(dir)
		
		run_pda(path, num_to_sample)
		
		os.chdir("../")
	
if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--tree_file', '-t', required=True,
						help='path of alignment file')
	parser.add_argument('--num_species', '-k', required=True,
						help='number of species to sample', type=int)
	parser.add_argument('-paths', action='store_true', 
						help='file contains paths')
	args = parser.parse_args()
	
	if args.paths:
		run_pda_paths(args.tree_file, args.num_species)
	else:
		run_pda(args.tree_file, args.num_species)

	