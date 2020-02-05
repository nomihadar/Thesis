import os
import sys
import csv
from ete3 import Tree
from run_treedist import treedist 

TRUE_TREE = "/groups/itay_mayrose/nomihadar/simulations/subtrees_of_simulated_seqs/subtrees_a/remove_species/true_tree.tree"
SIM_TREE = "/groups/itay_mayrose/nomihadar/simulations/subtrees_of_simulated_seqs/subtrees_a/remove_species/simulated.tree"

TRUE_TREE = "/groups/itay_mayrose/nomihadar/simulations/subtrees_of_simulated_seqs/subtrees_a/remove_species/true_tree.tree"
SIM_TREE = "/groups/itay_mayrose/nomihadar/simulations/subtrees_of_simulated_seqs/subtrees_a/remove_species/simulated.tree"


def prune_tree(tree, species_ls, output_name):

	tree.prune(species_ls, preserve_branch_length=True)
	tree.write(outfile = output_name, format = 1)
	
def main():

	true = Tree(TRUE_TREE)
	species = [node.name for node in true]
		
	output = [['number', 'species', 'distance']]	
	for i in range(len(true)):
		
		dir = 'species_' + str(i+1)
		os.makedirs(dir)
		os.chdir(dir)
		
		to_leave = [s for s in species if s != species[i]]
		
		true = Tree(TRUE_TREE)
		simulated = Tree(SIM_TREE)
		prune_tree(true, to_leave, "true_pruned.tree")
		prune_tree(simulated, to_leave, "simulated_pruned.tree")
		
		distance = treedist("true_pruned.tree", "simulated_pruned.tree")["bs"] #branch score
		
		output.append([str(i), species[i], str(distance)])

		os.chdir("../")
	    
	with open('summary.csv', 'w') as fp:
		csv_writer = csv.writer(fp, delimiter=',')
		csv_writer.writerows(output)


if __name__ == "__main__":

	if len(sys.argv) < 1:
		print "please insert argument"
		sys.exit(0)
	
	main()