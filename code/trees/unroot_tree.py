import argparse
from subprocess import call

def unroot(tree):

	if isinstance(tree, basestring):
		tree = Tree(tree, format = 1)
	
	if len(tree.children) == 2:
		if not tree.children[0].is_leaf():
			tree.children[1].dist += tree.children[0].dist
			tree.children[0].delete()
		elif not tree.children[1].is_leaf():
			tree.children[0].dist += tree.children[1].dist
			tree.children[1].delete()
	
def write(tree, outfile):
	tree.write(outfile =output,format = 1)
	
if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--tree', '-t', required=True,
						default = "", help='path to tree')
	parser.add_argument('--outfile', '-o', required=False,
						default = "unrooted.tree", help='outfile')
						
	args = parser.parse_args()
	tree = args.tree
	outfile = args.outfile
	
	unroot(tree)
	write(tree, outfile)	