import os, sys
import re

from get_tree_species import *
from rescale_branches import *

def extract_tree(filepath):

	#open file and extract the tree:
	with open (filepath, "r") as f:
		content = f.read()
		regex = re.search(r'(\(.*;)', content)
		tree = regex.group(0)
		
	return tree

def write_tree(fixed_tree, filename):

	with open(filename + ".nw", "w") as f:
		f.write(fixed_tree)
		f.write("\n")	
	
def main(filepath):

	# pda_paths = []
	# for filename in os.listdir(directory):
		# if filename.endswith(".nw"): 
			# filepath = os.path.join(directory, filename)
			# pda_paths.append(filepath)
		
	# for filepath in pda_paths:
	
	#extract tree from pda output 
	tree = extract_tree(filepath)
	
	regex = re.search(r'([0-9]+)_species.nw', filepath)
	num_species = regex.group(1)
	
	# dirname = num_species + "_species"
	# os.makedirs(dirname)
	# os.chdir(dirname)
	
	tree_name = "pda_output_tree_" + num_species + "_species"
	#convert branch lengths 
	fixed_tree = rescale_branches(tree)
	write_tree(fixed_tree, tree_name)
	
	get_tree_species(fixed_tree)
	
	# os.chdir("../")
		

if __name__ == "__main__":

	if len(sys.argv) < 2:
		print "please insert arguments"
		sys.exit(0)
		
	#get the path for the output dit
	pda_output = sys.argv[1]	
	
	main(pda_output)