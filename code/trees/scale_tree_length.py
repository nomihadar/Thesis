import sys
import os
from subprocess import call
from ete3 import Tree


OUTPUT = "scaled_by_{factor}_{user_output_name}.tree"

def scale_tree(tree_path, factor):
	
	tree = Tree(tree_path)
	
	for node in tree.traverse():
		node.dist *= 2
		
	return tree
	
def write_output(scaled_tree, factor, output):
	
	output_name = OUTPUT.format(factor=factor, user_output_name = output)
	scaled_tree.write(outfile = output_name, format = 1)
	
if __name__ == "__main__":

	if len(sys.argv) < 3:
		print "please insert arguments"
		sys.exit(0)
	
	tree_path = sys.argv[1]
	
	#list of species to prune 
	factor = int(sys.argv[2])
	
	output = sys.argv[3]
	
	scaled_tree = scale_tree(tree_path, factor)
	
	write_output(scaled_tree, factor, output)
	
	
	