import sys
from ete3 import NCBITaxa
from ete3 import Tree

"""
get all descendants in group as a tree
"""
def get_group_tree(group, rank):
	
	ncbi = NCBITaxa()
	
	translator = ncbi.get_name_translator([group])
	group_id = translator[group][0]
	
	# get an annotated tree
	tree = ncbi.get_descendant_taxa(group_id, collapse_subspecies=True, 
									return_tree=True)	
	
	return tree									
									
def get_species_by_rank(group, rank):
	
	ncbi = NCBITaxa()
	
	group_id = ncbi.get_name_translator([group])[group][0]

	# get an annotated tree
	tree = ncbi.get_descendant_taxa(group_id, collapse_subspecies=True, 
									return_tree=True)		
								
	dic_ids = {}
	dic_names = {}
	for node in tree.traverse("levelorder"):
		
		#if the rank of the current rank is the requested rank
		if node.rank == rank:
			#get its leaves
			leaves = node.get_leaves()
			#get their ids 
			dic_ids[node.taxid] = [leaf.taxid for leaf in leaves]
			dic_names[node.sci_name] = [leaf.sci_name for leaf in leaves]

	print "# of {rank}: {num}".format(rank = rank, num = len(dic_ids))	
	
	return dic_ids
	
def write_output(dic, group, rank):	

	output_file = "{group}_by_{rank}".format(group = group, rank = rank)

	#write to output file in format of group and species in that group (ids)
	with open(output_file, "w") as fout:	
		for key, tips in dic.iteritems():
			row = str(key) + ","
			row += ','.join(map(str, tips))
			fout.write(row)
			fout.write("\n")

	##write to output file in format of group and species in that group (names)
	# output_file += "_names"
	# with open(output_file, "w") as fout:	
		# for key, tips in dic_names.iteritems():
			# row = str(key) + ","
			# row += ','.join(tips)
			# fout.write(row)
			# fout.write("\n")
			

def get_species(tree):
	leaves = tree.get_leaves()
	leaves_ids = [leaf.taxid for leaf in leaves]
	return leaves_ids
	
	
# def read_tree(path):
	
	# tree = Tree(path, format = 1)
		
	##get all species in tree
	# species_names = [leaf.name.replace("_", " ") for leaf in tree]
	# print "num species in big tree ,", len(species_names)
	# name2taxid = ncbi.get_name_translator(species_names)
	# print "num species in big tree after conversion,", len(name2taxid)
	
	# return name2taxid.values()
			
			
if __name__ == "__main__":

	if len(sys.argv) < 3:
		print "please insert arguments"
		sys.exit(0)
	
	#get group to search in 
	group = sys.argv[1]
	
	#get rank
	rank = sys.argv[2]		
	
	#get the group tree
	#tree = get_group_tree(group, rank)	
	
	dic_ids = get_species_by_rank(group, rank)
	
	#write output
	write_output(dic_ids, group, rank)
	
	