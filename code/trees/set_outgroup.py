import sys
import os
from subprocess import call
from ete3 import Tree


def set_outgroup(tree_path, outgroup, output_name):
	
	tree = Tree(tree_path)
	tree.set_outgroup(tree&outgroup)
	tree.write(outfile = output_name, format = 1)
		
	
if __name__ == "__main__":

	if len(sys.argv) < 4:
		print "please insert arguments"
		sys.exit(0)
	
	tree_path = sys.argv[1]
	outgroup = sys.argv[2]
	output_name = sys.argv[3]

	set_outgroup(tree_path, outgroup, output_name)
	