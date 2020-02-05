import sys
from ete3 import NCBITaxa	
ncbi = NCBITaxa()

def get_species_of_clade(clade_id):

	species = ncbi.get_descendant_taxa(clade_id, collapse_subspecies=False, 
									return_tree=False)
	return species
	
if __name__ == "__main__":

	if len(sys.argv) < 2:
		print "please insert arguments"
		sys.exit(0)
	
	#get path to tree file
	clade_id = sys.argv[1]
	
	species = get_species_of_clade(clade_id)