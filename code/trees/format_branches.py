import sys
import argparse
from ete3 import Tree

def format_brances(tree_file):

	tree = Tree(tree_file)
	for node in tree.traverse():
		print str("{0:.10f}".format(node.dist))
		node.dist = str("{0:.10f}".format(node.dist))
		print node.dist
	
	return tree.write(format=1)
	
def write_tree(tree, output_name):
	
	with open(output_name, 'w') as f:
		f.write(tree)
		f.write("\n")
	
if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='')
						
	parser.add_argument('--tree_file', '-t', required=True,
						 help='path to tree')
						 
	parser.add_argument('--output_name', '-o', required=False,
						 default='formatted_branches.nw', help='output name')

	args = parser.parse_args()
	tree_file = args.tree_file
	output_name = args.output_name

	tree_str = format_brances(tree_file)
	write_tree(tree_str, output_name)