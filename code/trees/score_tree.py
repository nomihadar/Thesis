"""
Goal: 		Assessing the quality of the tree 
Input args: 1. a path to a tree file 
			2. group to search in 
			3. rank
			4. output name
Author:		Nomi Hadar
Date:		Januar 2016
"""

import csv
import sys
import numpy as np
import argparse
from ete3 import Tree #module load python/python-2.7.6
from ete3 import NCBITaxa

class Group:
	def __init__(self, taxid, species, species_intree, 
				score1=None, score2=None):
		self.taxid = taxid
		self.species = species 
		self.species_intree = species_intree #species found in tree
		self.score1 = score1
		self.score2 = score2
		self.num_species = len(species_intree)
	
	def score1ToStr(self):
		return "{:.3f}".format(self.score1)
		
	def score2ToStr(self):
		return "{:.3f}".format(self.score2)
		
	def toString(self):
	
		str = 'group id: {} \nspecies: {} \nspecies in tree: {} \nnum species: {}' \
				.format(self.taxid, self.species, 
						self.species_intree, self.num_species)
				
		if self.score1:
			str += '\nscore1: {:.3f} \nscore2: {:.3f}\n'\
				.format(self.score1, self.score2)
		else:
			str += '\nscore1: {} \nscore2: {}\n'\
					.format(self.score1, self.score2)
			
		return str
		


def write_output(groups, group, rank):

	out_file = "scores_{}_{}.csv".format(group, rank)
				
	out_log = "scores_{}_{}.logfile".format(group, rank)
	
	groups_ls = groups.values()
	groups_ls.sort(key = lambda group: group.num_species, reverse=True)
	
	with open(out_file, 'w') as fcsv:
		with open(out_log, 'w') as flog:
		
			csv_writer = csv.writer(fcsv)
			csv_writer.writerow(['group id','num species','score1','score2'])
			
			for group in groups_ls:
				
				flog.write(group.toString() + "\n")
				
				if group.species_intree:

					row = [str(group.taxid), str(group.num_species), 
							group.score1ToStr(), group.score2ToStr()]
					csv_writer.writerow(row)
					
def write_statistic(groups, group, rank):
		
	out_file = "scores_{}_{}_statistics.csv".format(group, rank)
			
	# data = [["minimal # species in group", "# groups", 
				# "score1 average", "score1 median", 
				# "score2 average", "score2 median", "# monophyly"]]
	
	data = [["minimal # species in group", "# groups", 
			"score1 average", "score1 std", 
			"score2 average", "score2 std", "# monophyly"]]
	
	for min_num in [5, 10, 20, 50, 100, 200, 500, 1000]:
		
		#ranks with minimal number of species:
		groups_filtered = [group for group in groups.values() 
							if group.num_species >= min_num]	
		
		if groups_filtered:
			row = stat(groups_filtered, min_num)
			data.append(row)
				
	with open(out_file, "w") as fout:
		fcsv = csv.writer(fout, delimiter=',')
		fcsv.writerows(data)
		
def stat(groups, min_num_species):
			
	#number of monophyly ranks
	num_monophyly = sum([1 for group in groups if group.score1 == 1])
	mono_percent = float(num_monophyly) / len(groups)
	
	#scores1 and their average
	scores1 = [group.score1 for group in groups]
	score1_avg = sum(scores1) / len(scores1)
	score1_std = np.std(scores1) 
	
	#scores2 and their average
	scores2 = [group.score2 for group in groups]
	score2_avg = sum(scores2) / len(scores2)
	score2_std = np.std(scores2) 
	
	row = [min_num_species, len(groups), 
			"{0:.3f}".format(score1_avg),
			"{0:.3f}".format(score1_std),			
			"{0:.3f}".format(score2_avg),
			"{0:.3f}".format(score2_std),				
			"{0:.3f}".format(mono_percent)]		
	
	return row
		
'''
score1: num of given species / num species in the tree of the common ancestor
'''
def calc_score1(common_ancestor, species):
	
	#len of node is number of leaves (species)
	score = float(len(species)) / len(common_ancestor)
	return score

'''
score2: the largest monophyly group in the common ancestor
'''
def calc_score2(common_ancestor, species):
	
	score = 0
	
	#traverse the common ancestor's tree in postorder
	for node in common_ancestor.traverse("postorder"):
	
		#if node is a species, check weather it is in the given species list
		if node.is_leaf():
		
			#if species in group, include = 1 and out = 0, o.w the opposite 
			node.add_feature("include", int(node.name in species))
			node.add_feature("out", int(not node.include))
		else:
			
			in_sum = node.children[0].include + node.children[1].include  
			out_sum = node.children[0].out + node.children[1].out
			
			# include: number of children in group, 
			#out: number of children out of group
			node.add_feature("include", in_sum)
			node.add_feature("out", out_sum)
	
	#from the common ancestor's tree get only the monophyly nodes 
	#(those with out == 0)
	monophyly_nodes = common_ancestor.search_nodes(out=0)
	sizes = [node.include for node in monophyly_nodes if not node.is_leaf()]
	if sizes:
		max_monophyly_size = max(sizes)
		score =  max_monophyly_size / float(len(species))
	
	return score

def calculate_scores(tree, groups):	

	# for each group of species calculate its monophyly_score
	for group_id, group in groups.iteritems():
		
		species = group.species_intree
	
		#if there are not species in that group 
		if not len(species):
			continue
		
		is_mono = tree.check_monophyly(values=species, target_attr="name")
		
		if is_mono is True:
			group.score1 = 1
			group.score2 = 1
		
		else:
		
			#get the first internal node grouping all given species
			if len(species) == 1:
				common_ancestor = (tree&species[0]).up
			else:
				common_ancestor = tree.get_common_ancestor(species)
			
			#calculate scores
			group.score1 = calc_score1(common_ancestor, species)
			group.score2 = calc_score2(common_ancestor, species)
	
"""
get species by rank, only species found in the input tree 
and create a groups dictionary 
take ony
"""
def get_species_by_rank(input_tree, group, rank):
	
	#get species of input tree
	tree_taxa = [leaf.name for leaf in input_tree]
	
	ncbi = NCBITaxa()
	
	#convert group name to id 
	group_id = ncbi.get_name_translator([group])[group][0]
	
	#get an annotated tree
	tree = ncbi.get_descendant_taxa(group_id, collapse_subspecies=True, 
									return_tree=True)
	
	groups = {}
	for node in tree.traverse("levelorder"):
		
		#if the rank of the current rank is the requested rank
		if node.rank == rank:
			
			#get node's species and subspecies ids 
			descen = list(ncbi.get_descendant_taxa(node.taxid,
						collapse_subspecies=False, return_tree=False)) #species
			descen2 = list(ncbi.get_descendant_taxa(node.taxid,
						collapse_subspecies=True, return_tree=False))  #species/varietas
			descendants = list(set(descen).union(descen2))			
			
			#to string 
			species = [str(descendant) for descendant in descendants] 
			
			#remove species not found in the input tree 
			species_intree = [s for s in species if s in tree_taxa]
			
			#create a group 
			group = Group(taxid = node.taxid, species = species, 
							species_intree = species_intree)
			
			#add group to dictionary 
			groups[node.taxid] = group
			
	return groups

def main(tree_path, group, rank):

	# Load a tree from a file , format =1
	input_tree = Tree(tree_path, format =1)

	#get a dict of rank and species under that rank 
	groups = get_species_by_rank(input_tree, group, rank)
	
	#calculate scores
	calculate_scores(input_tree, groups)	
	
	#write output
	write_output(groups, group, rank)
	
	#write statistic
	write_statistic(groups, group, rank)

	
if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='')
	parser.add_argument('-tree', required=True) #get path to tree file
	parser.add_argument('-group', required=True) #get group to search in
	parser.add_argument('-rank', required=True) #get rank
	
	args = parser.parse_args()
	print args.tree
	main(args.tree, args.group, args.rank)
	
	