import os, sys
from collections import Counter

class Species:
	def __init__(self, list_name, species, species_in_cover = None):
		self.list_name = list_name
		self.species = species
		self.species_in_cover = species_in_cover
		
		
	def get_num_species(self):
		return len(self.species)
		
	def get_num_species_in_cover(self):
		return len(self.species_in_cover)

def read_lists(paths_lists):

	with open(paths_lists, 'r') as fin:
		paths = fin.read().splitlines()

	lists = []
	
	for path in paths:
		print path 
		with open(path, 'r') as f:
			species = f.read().splitlines()
			
		#get the name of the alignment file 
		file_name = os.path.basename(path)
		
		species_obj = Species(file_name, species)
		
		lists.append(species_obj)
	
	return lists
	
def filter_by_cover(lists, min_genes):

	all_species = []
	for list_name, list in lists.iteritems():
		all_species.extend(list) 
	
	#counter 
	counter = dict(Counter(all_species))
	
	filtered_lists = {}
	for list_name, list in lists.iteritems():
		filtered = [species	for species in list 
					if counter[species] >= min_genes]
			
		filtered_lists[list_name] = filtered
		
	return filtered_lists
	
def write_output(lists, lists_unfiltered, min_genes):
	
	all_species = []
	for list_name, list in lists.iteritems():
		all_species.extend(list) 
	
	
	with open("filter_by_cover.ls", 'w') as f:
		for list_name, list in lists.iteritems():
			f.write('\n'.join(list) + '\n')
	
	# with open("filter_by_cover_logfile", 'w') as f:
		# for list_name, list in lists.iteritems():
			# f.write('\n'.join(list) + '\n')
	
	print "gene		num_species_before		num_species_after"
	for list_name, list in lists.iteritems():
		
		before_size = len(lists_unfiltered[list_name])
		
		print "{}{: >5}{: >5}\n".format(list_name, before_size, len(list))

		with open(list_name, 'w') as f:
			f.write('\n'.join(list) + '\n')
			
if __name__ == "__main__":

	if len(sys.argv) < 3:
		print "please insert argument"
		sys.exit(0)
	
	#paths of lists 
	paths_lists = sys.argv[1]
	
	#minmal number of genes 
	min_genes = int(sys.argv[2])
	
	lists = read_lists(paths_lists)

	filtered_lists = filter_by_cover(lists, min_genes)
	
	write_output(filtered_lists, lists, min_genes)
	