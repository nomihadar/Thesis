from __future__ import division
import os, sys
import argparse
import re
import pandas as pd
from Bio import SeqIO 
from ete3 import Tree
from subprocess import call

sys.path.append("/groups/itay_mayrose/nomihadar/code/")

import run_job as rj


def read_log(log_file, insertions, deletions):
	with open(log_file,'r') as f:
		content = f.read()
		
	#get number of indel events and average length	
	n_insert = re.search(r'insertion events\s+(\d+)', content).group(1)
	n_delet = re.search(r'deletion events\s+(\d+)', content).group(1)
	len_insert = re.search(r'insertion length\s+([-+]?\d*\.\d+|\d+|-nan)', content).group(1)
	len_delet = re.search(r'deletion length\s+([-+]?\d*\.\d+|\d+|-nan)', content).group(1)

	#my counting
	my_len_insert = sum(insertions) / len(insertions) if len(insertions) else None
	my_len_delet = sum(deletions) / len(deletions) if len(deletions) else None
	real = [n_insert, len_insert, n_delet, len_delet]
	estimated = [len(insertions), my_len_insert, len(deletions), my_len_delet]
	data = [real, estimated]
	df = pd.DataFrame(data, columns = ['insertions', 'len', 'deletions', 'len'], 
						index = ["real", "estimated"])
	print df
	#df.to_csv(output)
	
def read_tree(tree_file):
	with open(tree_file,'r') as f:
		content = f.read()
	tree = re.search(r'(\(.*\)ROOT;)', content).group(1)
	return tree
	
def read_msa(msa_file):
	
	with open(msa_file,'r') as f:
		lines = f.read().splitlines()
	
	seqs = {}	
	for line in lines[1:-1]:
		splited = line.split()
		seqs[splited[0]] = splited[1]
	
	return seqs
	
def find_insertions(seq1, seq2):

	lengths = []
	for m in re.finditer('[actg]+', seq1):
		subseq1 = m.group()
		subseq2 = seq2[m.start():m.end()]
		regex = re.finditer('[^actg]+', subseq2)
		ls = [len(r.group()) for r in regex]	
		lengths.extend(ls)
	print "insertions: ", lengths	
	return lengths
			
def find_deletions(seq1, seq2):

	lengths = []
	for m in re.finditer('[-*]+', seq1):
		subseq1 = m.group()
		subseq2 = seq2[m.start():m.end()]
		
		regex = re.finditer('[ACTGactg]+', subseq2)
		ls = [len(r.group()) for r in regex]	
		lengths.extend(ls)
		#print subseq1, subseq2,lengths
	print "deletions: ", lengths
	return lengths
	
def main(tree_file, msa_file, log_file):
	
	tree = Tree(read_tree(tree_file), format =1)
	print tree.get_ascii()
	seqs = read_msa(msa_file)
	
	insertions = []
	deletions = []
	for node in tree.traverse("preorder"):
		
		if node.is_leaf():
			continue
	
		seq = seqs[node.name]
		#for each child 
		for child in node.children:
			child_seq = seqs[child.name]
			print "({},{})".format(child.name, node.name)
			
			insertions.extend(find_insertions(child_seq, seq))
			deletions.extend(find_deletions(child_seq, seq))			
	
	read_log(log_file, insertions, deletions)
	#check deletions

	
	
if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--tree_file', '-t', required=True,
						help='tree file from "trees.txt" outputed by indelibe')
	parser.add_argument('--msa_file', '-m', required=True, help='msa file')
	parser.add_argument('-log', required=False, help='log file of indelible')
						
	args = parser.parse_args()
	
	main(args.tree_file, args.msa_file, args.log)
	
