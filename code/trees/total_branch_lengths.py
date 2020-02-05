import argparse
from ete3 import Tree

def total_branches_lengths(tree):
	
	if isinstance(tree, basestring):
		tree = Tree(tree_path)
	
	return sum([node.dist for node in tree.traverse()])
		

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--tree', '-t', required=True, help='path of tree')
	args = parser.parse_args()
	tree_path = args.tree
	
	total = total_branches_lengths(tree_path)
	
	print total 
