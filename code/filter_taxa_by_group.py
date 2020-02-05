"""
script name:	filter_taxa_by_group.py
description:	get a list of taxa names or ids and a group, 
				and remove those who are not found in the list  
arguments:		1. a list of taxa names/ids 
				2. a group name 
				3. an output name 
output:			list of species in group 
cmd:			python ~/code/filter_taxa_by_group.py taxa.ls fabaceae output_name
"""

import sys
import os
from ete3 import NCBITaxa
from ete3 import Tree

"""
read taxons names and convert to ids
"""
def read_taxons(taxons_path):
	
	ncbi = NCBITaxa()
	
	with open(taxons_path, 'r') as fin:
			taxons = fin.read().splitlines()
	
	#if list of ids - convert ids to ints
	try:
		taxons_ids = [int(id) for id in taxons]
	
	#else - list of names - convert names to ids 
	except ValueError:
		
		#dictionary name to id 
		name2taxid = ncbi.get_name_translator(taxons)
		
		taxons_ids = []
		for name, ids in name2taxid.iteritems():
			taxons_ids.extend(ids)
	
	return taxons_ids
	

"""
return a list of taxons in group
"""
def filter(group, taxons_ids):
	
	ncbi = NCBITaxa()
	
	group_id = ncbi.get_name_translator([group])[group][0]
	
	filtered = []
	
	for id in taxons_ids:
		lineage = ncbi.get_lineage(id)
		if group_id in lineage:
			filtered.append(id)

	return filtered	

	
def write_output(filtered, output_name):
	
	with open(output_name, 'w') as fout:
		for id in filtered:
			fout.write(str(id) + "\n")

if __name__ == "__main__":

	if len(sys.argv) < 4:
		print "please insert arguments"
		sys.exit(0)
	
	#get type of file (fasta / phylip)
	taxons_path = sys.argv[1]
	
	#get path to alignment file
	group = sys.argv[2]
	
	#get output name 
	output_name = sys.argv[3]
	
	taxons_ids = read_taxons(taxons_path)
	
	filtered = filter(group, taxons_ids)
	
	write_output(filtered, output_name)
	

#intersection = intersection(group, taxons)
# def intersection(group, taxons):
	
	# ncbi = NCBITaxa()
	
	##get group's descendants and thier names
	# descendants = ncbi.get_descendant_taxa(group) #missing sime species

	# descendants_names = ncbi.translate_to_names(descendants)

	# intersection = [name for name in taxons if name in descendants_names]
	
	# return intersection