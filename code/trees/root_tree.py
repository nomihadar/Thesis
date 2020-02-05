import sys
import os
from subprocess import call
from ete3 import Tree

def root_tree(tree_path, species_path, output_name):
	
	with open (species_path, 'r') as f:
		species_list = f.read().splitlines() 

	tree = Tree(tree_path)
	ancestor = tree.get_common_ancestor(species_list)
	tree.set_outgroup(ancestor)
	tree.write(outfile = output_name, format = 1)
		
if __name__ == "__main__":

	if len(sys.argv) < 4:
		print "please insert arguments"
		sys.exit(0)
	
	tree_path = sys.argv[1]
	species_path = sys.argv[2]
	output_name = sys.argv[3]

	root_tree(tree_path, species_path, output_name)
	