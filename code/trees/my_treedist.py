import os
import sys
import argparse
import math
from ete3 import Tree

def partition_to_str(partition):
	a, b = partition
	return '(' + ','.join(a) + ' | ' + ','.join(b) + ')'

def tree_to_str(tree):
	return tree.get_ascii(attributes=["name", "dist"], show_internal=True)
	
def total_branches_lengths(tree, is_path = True):
	return sum([node.dist for node in tree.traverse()])
	
def get_branch(tree, split):
	a, b = split	
	if len(a) == 1:
		branch = (tree&a[0]).dist
	elif len(b) == 1:	
		branch = (tree&b[0]).dist
	else:
		ancestor_a = tree.get_common_ancestor(a) 
		branch = ancestor_a.dist
		if ancestor_a.is_root() or \
			(ancestor_a.up is not None and ancestor_a.up.is_root()):
			branch += tree.get_common_ancestor(b).dist
	
	return branch
	
def treedist(tree1, tree2, output_file="treedist_output", write_logfile = True):

	tree1 = Tree(tree1)
	tree2 = Tree(tree2)

	rf = tree1.robinson_foulds(tree2, unrooted_trees=True)
	splits_t1 = list(rf[3])
	splits_t2 = list(rf[4])

	common = [(s,0) for s in splits_t1 if s in splits_t2]
	t1_splits = [(s,1) for s in splits_t1 if s not in splits_t2]
	t_2_splits = [(s,2) for s in splits_t2 if s not in splits_t1]
	splits = common + t1_splits + t_2_splits

	output = []
	for split, tree in splits:
		
		a, b = split
		if not a or not b:
			continue
		
		if tree == 0:
			dist1 = get_branch(tree1, split)
			dist2 = get_branch(tree2, split)
		if tree == 1:
			dist1 = get_branch(tree1, split)
			dist2 = 0
		if tree == 2:
			dist1 = 0
			dist2 = get_branch(tree1, split)
			
		if tree:
			sub = "{}^2".format(max(dist1, dist2))
		else:
			sub = "({}-{})^2".format(dist1, dist2)
		
		differ = (dist1 - dist2)**2
		
		output.append([len(a), len(b), partition_to_str(split), 
							sub, differ])
	
	differs = [d[4] for d in output]
	dist = math.sqrt(sum(differs)) #final answer
	
	if write_logfile:
		with open(output_file, 'w') as f:
			f.write("distance: {}\n".format(dist))
			for row in output:
				f.write(','.join(map(str,row)) + "\n")
	
	return dist

	
if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description='')
	
	parser.add_argument('--tree1', '-t1', required=True, 
						help='path of first tree')
	
	parser.add_argument('--tree2', '-t2', required=True, 
						help='path of second tree')
						
	parser.add_argument('--output', '-o', required=False,
						default = "treedist_output", help='output name')
	
	args = parser.parse_args()
	path1 = args.tree1
	path2 = args.tree2
	output = args.output

	treedist(path1, path2, output)