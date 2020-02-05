import sys
import os
from random import randint
from ete3 import Tree, NodeStyle, TreeStyle #module load python/python-2.7.6

DIFFERENCE = 18

class Subtree:
	def __init__(self, tree):
		self.tree = tree
		self.species = [leaf.name for leaf in self.tree]
		
	def write(self, output_name):
		self.tree.write(outfile = output_name, format = 1)
		
	def speciesToStr(self):
		return '\n'.join(self.species)
	
	def markSpeciesOnTree(self, tree, output_name):
	
		for species in self.species:
			nstyle = NodeStyle()
			nstyle["bgcolor"] = "purple"
			(tree&species).set_style(nstyle)

		ts = TreeStyle()
		#ts.mode = "c"	
		ts.scale = 500
		#tree.show(tree_style=ts)			
		tree.render(output_name, dpi = 300,units="mm", tree_style=ts)
		

def write_output(subtrees, input_tree):

	for i, subtree in enumerate(subtrees):
	
		#write subtree in newick format 
		output_subtree = "subtree_{i}.tree".format(i=i+1)
		subtree.write(output_subtree)
		
		#write species to file 
		output_species = "subtree_{i}.ls".format(i=i+1)			
		with open(output_species, 'w') as fout:
			fout.write(subtree.speciesToStr() + '\n')
		
	with open("logfile", 'w') as fout:
		for i, subtree in enumerate(subtrees):
			row = "subtree {i}: {num_species} species\n"\
					.format(i=i+1, num_species = len(subtree.species))
			fout.write(row)
		
		
		'''
		#mark species on input tree  
		output_image = "subtree_{i}_{num_species}_species.png"\
						.format(i=i+1, num_species = len(subtree.species))
		subtree.markSpeciesOnTree(input_tree, output_image)
	'''
	
def get_subtrees(tree, num_subtrees):
		
	#get tree leaves
	leaves = tree.get_leaves()
	
	#get a random leaf
	node = leaves[randint(0,len(tree))]
	upper_node = node.up
	
	subtrees = [] 
	while True:
	
		#if we got the root or if we got the requested number of subtrees:
		if upper_node == tree or len(subtrees) == num_subtrees:
			break
			
		if len(upper_node) - len(node) >= DIFFERENCE: 
			subtrees.append(Subtree(upper_node))
			node = upper_node
				
		upper_node = upper_node.up
		
	return subtrees

def main(tree_path, num_subtrees):	

	#load a tree from a file , format =1
	tree = Tree(tree_path, format=1)
	
	#get subtrees
	subtrees = get_subtrees(tree, num_subtrees)
	
	write_output(subtrees, tree)
	
if __name__ == "__main__":

	if len(sys.argv) < 3:
		print "please insert arguments"
		sys.exit(0)
	
	tree_path = sys.argv[1]
	num_subtrees = int(sys.argv[2])
	
	main(tree_path, num_subtrees)
	