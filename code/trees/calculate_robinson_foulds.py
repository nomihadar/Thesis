import os
import sys
from ete3 import Tree

def calculate_distance(tree1_path, tree2_path):

	t1 = Tree(tree1_path, format = 1)
	t2 = Tree(tree2_path, format = 1)
	
	results = t1.robinson_foulds(t2, unrooted_trees = True)
	rf = results[0]
	print rf
	#rf, max_rf, common_leaves, parts_t1, parts_t2
	#print rf, max_rf, common_leaves, parts_t1, parts_t2
	
	return rf


if __name__ == "__main__":

	if len(sys.argv) < 3:
		print "please insert argument"
		sys.exit(0)
		
	tree1_path = sys.argv[1]
	tree2_path = sys.argv[2]
	
	rf = calculate_distance(tree1_path, tree2_path)