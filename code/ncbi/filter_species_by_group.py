import sys
from ete3 import NCBITaxa
from ete3 import Tree


MONOCOTS = "Liliopsida"
DICOTS = "eudicotyledons"

def read_species(species_path):
	
	with open (species_path, 'r') as f:
		species_ls = f.read().splitlines() 

	return species_ls

def filter_species(species_ids, group):
	
	ncbi = NCBITaxa()
	
	group_id = ncbi.get_name_translator([group])[group][0]
	
	filtered_ids = []
	for species_id in species_ids:
		lineage = ncbi.get_lineage(species_id)
		
		print species_id, lineage
		
		if group_id in lineage:
			filtered_ids.append(species_id)

	return filtered_ids
	
def write_output(filtered_ids, group, output_file):	

	#output_file = "species_of_{group}.ls".format(group = group)

	#write to output file in format of group and species in that group (ids)
	with open(output_file, "w") as fout:	
		ls = '\n'.join(map(str,filtered_ids))
		fout.write(ls)
			
def main(species_path, group, output_file):
	
	species_ids = read_species(species_path)
	filtered_ids = filter_species(species_ids, group)		
	write_output(filtered_ids, group, output_file)
	
if __name__ == "__main__":

	if len(sys.argv) < 4:
		print "please insert arguments"
		sys.exit(0)
	
	#get group to search in 
	species_path = sys.argv[1]
	
	#get rank
	group = sys.argv[2]		
	
	output_file = sys.argv[3]	
	
	main(species_path, group, output_file)
	

	