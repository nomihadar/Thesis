import os
import sys
from ete3 import Tree


def write_tree(common_ancestor, output_name):	
	common_ancestor.write(outfile = output_name, format = 1)

def write_species(common_ancestor, output_name):
	
	with open(output_name, 'w') as fout:
	
		for leaf in common_ancestor:
			fout.write(leaf.name + "\n")
	
def main(tree_path, species_path):
	
	tree = Tree(tree_path, format=1)
	
	with open (species_path, 'r') as f:
		species = f.read().splitlines() 

	#get the first internal node grouping all given species
	common_ancestor = tree.get_common_ancestor(species)
	
	return common_ancestor
	
	
if __name__ == "__main__":

	if len(sys.argv) < 4:
		print "please insert argument"
		sys.exit(0)
	
	#get path to tree file
	tree_path = sys.argv[1]
	
	species_path = sys.argv[2]
	
	output_name = sys.argv[3]
	
	mode = sys.argv[4]
	
	common_ancestor = main(tree_path, species_path)
	
	if mode == "tree":
		write_tree(common_ancestor, output_name)
	
	if mode == "species":
		write_species(common_ancestor, output_name)
	
	
	
	
	