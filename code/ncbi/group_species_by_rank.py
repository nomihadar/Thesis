import sys
import numpy as np
from ete3 import Tree #module load python/python-2.7.6
from ete3 import NCBITaxa

sys.path.append("/groups/itay_mayrose/nomihadar/code/")

class Group:
	def __init__(self, taxid, species):
		self.taxid = taxid
		self.species = species 	

def read_species_list(path):		
	with open (path, 'r') as f:
		species_list = f.read().splitlines() 	
	return species_list

def write_output(groups, output_name, rank):
		
	with open(output_name, 'w') as f:
	
		num_species = sum([len(group.species) for group in groups])
		sum_line = "num {}s: {}\nnum species in total:{}\n\n"\
				.format(rank, len(groups), num_species)
		f.write(sum_line)
	
		title = '{0: <12}{1:}\n'.format(rank, "species")
		f.write(title)
		for group in groups:
			line = '{0: <12}{1:}\n'\
					.format(group.taxid, ', '.join(group.species))
			f.write(line)
		
def get_species_by_rank(species_list, group, rank):
	
	ncbi = NCBITaxa()
	
	#convert group name to id 
	group_id = ncbi.get_name_translator([group])[group][0]

	#get an annotated tree
	tree = ncbi.get_descendant_taxa(group_id, collapse_subspecies=True, 
									return_tree=True)
	
	groups = []
	for node in tree.traverse("levelorder"):
		
		#if current rank is the requested rank
		if node.rank == rank:
			
			#get node's species ids 
			species = [str(leaf.taxid) for leaf in node.get_leaves()]
			
			#remove species not found in the species list  
			species_inlist = [s for s in species if s in species_list]
	
			if species_inlist:
				#create a group 
				group = Group(taxid = node.taxid, species = species_inlist)
				
				#add group to dictionary 
				groups.append(group)
				
	return groups

if __name__ == "__main__":

	if len(sys.argv) < 5:
		print "please insert arguments"
		sys.exit(0)
	
	#path to species list 
	list_path = sys.argv[1]
	
	#get group to search in 
	group = sys.argv[2]
	
	#get rank
	rank = sys.argv[3]		
	
	#output name 
	output_name = sys.argv[4]

	species_list = read_species_list(list_path)
	
	groups = get_species_by_rank(species_list, group, rank)
	
	write_output(groups, output_name ,rank)
	
	