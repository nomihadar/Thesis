import csv
import sys
import numpy as np

from ete3 import  Tree, NodeStyle, TreeStyle, TextFace
from ete3 import NCBITaxa

def read_species(species_path):		
	with open (species_path, 'r') as f:
		species_list = f.read().splitlines() 	
	return species_list

def mark_species_on_tree(tree, species):
	
	for species in species:
		nstyle = NodeStyle()
		nstyle["bgcolor"] = "purple"
		(tree&species).set_style(nstyle)

def show_tree(tree):

	ts = TreeStyle()
	ts.scale = 1
	ts.show_leaf_name = True
	
	'''
	ts.rotation = 90
	ts.branch_vertical_margin = 10
	ts.scale = 50
	'''
	
	#ts.mode = "c"

	tree.show(tree_style=ts)
	#tree.render(output_name, dpi =300, units="mm", tree_style=ts)
	
	
def main(tree_path):	

	tree = Tree(tree_path, format =1)
	#species = read_species(species_list)
	
	show_tree(tree)
	
	#mark_species_on_tree(tree, species)
	
if __name__ == "__main__":

	if len(sys.argv) < 2:
		print "please insert arguments"
		sys.exit(0)
	
	#get path to tree file
	tree_path = sys.argv[1]
	
	if len(sys.argv) > 3:
		#get species to mark
		species_list = sys.argv[2]
		output_name = sys.argv[3]
	
	
	main(tree_path)
	