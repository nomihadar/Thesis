import sys
import os
import re 
import csv
from numpy import genfromtxt
from collections import defaultdict
from pprint import pprint
from ete3 import Tree
#module load python/python-3.3.0

#"/groups/itay_mayrose/nomihadar/ncbi_taxonomy_data/nodes.dmp"
NCBI_NODES_PATH = "/groups/itay_mayrose/nomihadar/tests/mynodes.dmp"
NCBI_NAMES_PATH = ""

#num columns
TAX_ID = 0 
PARENT_TAX_ID = 1
RANK = 2

def tree(): return defaultdict(tree)

def tree_add(t, path):
  for node in path:
    t = t[node]

def pprint_tree(tree_instance):
    def dicts(t): return {k: dicts(t[k]) for k in t}
    pprint(dicts(tree_instance))

def csv_to_tree(input):
    t = tree()
    for row in csv.reader(input, quotechar='\''):
        tree_add(t, row)
    return t
	
def lineages_to_tree(lineages):
    t = tree()
    for lineage in lineages:
        tree_add(t, lineage)
    return t

def tree_to_newick(root):
    items = []
    for k in root.keys():
        s = ''
        if len(root[k].keys()) > 0:
            sub_tree = tree_to_newick(root[k])
            if sub_tree != '':
                s += '(' + sub_tree + ')'
        s += str(k)
        items.append(s)
    return ','.join(items) 

def csv_to_weightless_newick(lineages):
    t = lineages_to_tree(lineages)
    #pprint_tree(t)
    return tree_to_newick(t)


class Node():

	def __init__(self, id, parent_id, lineage =[]):
		self.id = id
		self.parent_id = parent_id
		self.rank = rank
		self.lineage = lineage
	
	def __str__(self):
		return "id: {id} rank: {rank}" \
				.format(id = str(self.id), rank = self.rank) 
	
	def print_lineage(self):
		
		print (str(self.lineage))
		
"""
read nodes file and returns dic of Nodes
"""
def read_nodes():
	
	#reas the columns of tax id and parent tax id
	taxes_ids = genfromtxt(NCBI_NODES_PATH, delimiter='|', 
						usecols=(TAX_ID, PARENT_TAX_ID), dtype=(int,int))
	
	#read ranks column	
	ranks = genfromtxt(NCBI_NODES_PATH, delimiter='|', 
						usecols=(RANK), dtype=(str))
	
	# remove spaces from ranks 
	#for i, rank in enumerate(ranks):
	#	ranks[i] = rank.strip()
		
	#create a dictionary of nodes with tax_id as key 
	ids = taxes_ids[:,0]
	parents_ids = taxes_ids[:,1]
	
	nodes = {}
	for id, parent_id, rank in zip(ids, parents_ids, ranks):
		nodes[id] = Node(id, parent_id, rank.strip())
	
	return (nodes, taxes_ids)

"""
get nodes of requested rank 
"""
def filter_by_rank(nodes, taxes_ids, rank):
	
	parents_ids = taxes_ids[:,1]
	
	filtered_nodes = {}
	for id, node in nodes.items():
				
		if node.rank is rank:
			filtered_nodes[id] = node 	
	
	return filtered_nodes		
	
"""
for each node get its lineage within the input group
"""	
def find_lineages(nodes, group_id):

	#for each node
	for id, node in nodes.items():
		
		lineage = []
		
		#while node  
		new_id = id
		while True:
			
			lineage.append(new_id)
			
			#new id is the parent of current node
			new_id = nodes[new_id].parent_id
			
			#stop condition 
			if new_id is nodes[new_id].parent_id:
				break
		
		#add lineage to node 
		node.lineage = reversed(lineage)

	
if __name__ == "__main__":

	if len(sys.argv) < 2:
		print ("please insert arguments")
		sys.exit(0)
	
	#get a group within which to resolve query
	group_id = int(sys.argv[1])
	
	#a Linnaean rank to restrict taxonomic resolution
	rank = sys.argv[2]

	#get path to names.dmp
	#name_path = sys.argv[2]
	
	#read nodes 
	(nodes, taxes_ids) = read_nodes()
	
	#get nodes by input rank 
	filtered_nodes_dic = filter_by_rank(nodes, taxes_ids, rank)
	
	filtered_nodes_dic = nodes
	#group id 
	#nodes_dic[group_id].rank
	
	#for each node find its lineage 
	find_lineages(filtered_nodes_dic, taxes_ids)
	
	lineages = []
	for id, node in nodes.items():
		lineages.append(node.lineage)
		#print (str(node))
	
	tree = csv_to_weightless_newick(lineages)		
		
	
	t = Tree(tree + ";", format = 8)
	print (t)
	
	for node in t.traverse("postorder"):

		print (node.name)
	
	print (t.get_node_by_name("12"))
	