import os, sys
from subprocess import call
from ete3 import Tree
import argparse

def prune_tree(tree_path, species_path, output_name):
		
	with open (species_path, 'r') as f:
		species_ls = f.read().splitlines() 
		
	try:
		tree = Tree(tree_path)
	except:
		print "file {} was not found".format(tree_path)	
		sys.exit(0)
		
	tree = Tree(tree_path)
	
	tree_species = [l.name for l in tree]
	
	species = set(tree_species).intersection(species_ls)
	
	tree.prune(species, preserve_branch_length=True)
	
	tree.write(outfile = output_name, format = 1)
	
if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description='')
	
	parser.add_argument('--tree_path', '-t', required=True,
						help='path of the tree')
	
	parser.add_argument('--species_path', '-s', required=True,
						help='list of species to prune')
	
	parser.add_argument('--output_name', '-o', required=False,
						help='output name', default = "pruned.tree")

	args = parser.parse_args()
	tree_path = args.tree_path
	species_path = args.species_path
	output_name = args.output_name
	
	prune_tree(tree_path, species_path, output_name)
	
	