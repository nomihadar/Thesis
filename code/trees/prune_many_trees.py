import sys
import os
from subprocess import call
from ete3 import Tree

TREE_PATH = "/groups/itay_mayrose/nomihadar/simulations/repeats_trees_ericaceae/equal_num_genes/subfamily_217035/subfamily_217035_{i}/tree_mafft/ExaML_result.subfamily_217035_{i}"

"/groups/itay_mayrose/nomihadar/simulations/subtrees_of_simulated_seqs/subtrees_a/subtree_10_3368_species/subtree_10_1/tree_mafft/ExaML_result.subtree_10_1"

def main(species_path):

	with open (species_path, 'r') as f:
		species_ls = f.read().splitlines() 

	for i in range(1,100):
	
		tree_path = 
		.format(i=i)
		tree = Tree(tree_path)
		
		tree.prune(species_ls, preserve_branch_length=True)
		
		output_name = TREE_PATH.split(".")[1].format(i=i) + "_pruned.tree"
		tree.write(outfile = output_name, format = 1)
	
	print "trees were pruned from:\n"
	print TREE_PATH
	
if __name__ == "__main__":

	if len(sys.argv) < 2:
		print "please insert arguments"
		sys.exit(0)
	
	#list of species to prune 
	species_path = sys.argv[1]
	
	main(species_path)

	
	
	
	
	