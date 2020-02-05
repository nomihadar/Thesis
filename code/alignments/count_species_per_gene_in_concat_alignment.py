import sys
import os
import numpy as np
import re 
import csv
from itertools import izip_longest

class Gene:
   
   def __init__(self, name, start, end, seqs = {}):
		self.name = name	#gene name 
		self.start = start 	#partition 
		self.end = end	   	#partition 
		self.seqs = seqs	#dict of species (key) and seq (value) 
		
   def displayGene(self):
		print "Name: ", self.name, "start: ", \
				self.start, "end: ", self.end, "msa: ", self.seqs
		

#read partitions file
def read_partitions(partition_path):
	
	partitions = np.loadtxt(partition_path, delimiter = " ", 
							dtype = 'str')
	genes = []
	for _, gene, _, positions in partitions:
		(start, end) = positions.split("-")
		genes.append(Gene(gene, int(start)-1, int(end)))

	# with open(partition_path, 'r') as f:
		
		# for line in f:
			# regex = re.search(" (.*) = ([1-9]*)-([1-9]*)", line.strip())
			# gene = regex.group(1)
			# start = int(regex.group(2))-1
			# end = int(regex.group(3))
			
	return genes
	
#read seqs 
def read_seqs(type, align_path):
	
	#read sequences (in pylip format)
	seqs_dic = {}

	with open(align_path) as f:
		for i, line in enumerate(f):
			if i == 0:
				continue
			
			splited = line.split()
			if splited:
				species = splited[0]
				conc_seqs = splited[1]
				seqs_dic[species] = conc_seqs
	
	return seqs_dic

def count_seqs(genes, seqs_dic):
	
	#for each gene
	for gene in genes:
		
		#get the msa of current partiotin 
		seqs = {}
		for species, concat_seq in seqs_dic.iteritems():
			
			#get the sequence from the concat sequence
			seq = concat_seq[gene.start:gene.end]
			
			#if the sequence is not empty add it to the dictionary
			if len(seq) != seq.count('-'):	
				seqs[species] = seq 	

		gene.seqs = seqs #add to gene variables 

def write_output(genes, align_path):

	genes_names = [gene.name for gene in genes]
	species_list = [sorted(gene.seqs.keys()) for gene in genes]
	
	with open("num_species_per_gene.csv", 'w') as f:
		writer = csv.writer(f)
		f.write("file path: " + align_path + "\n\n")
		
		writer.writerow(["gene name","num species"])
		for gene in genes:
			row = [gene.name, len(gene.seqs)]
			writer.writerow(row)
			
	with open("list_species_per_gene.csv", 'w') as f:
		writer = csv.writer(f)
		writer.writerow(genes_names)
		for values in izip_longest(*species_list):
			writer.writerow(values)
			
	
if __name__ == "__main__":

	if len(sys.argv) < 3:
		print "please insert arguments"
		sys.exit(0)
	
	#get type of file (fasta / phylip)
	file_type = sys.argv[1]
	
	#get path to alignment file
	align_path = sys.argv[2]
	
	#get path to the partiotins file  
	partition_path = sys.argv[3]
	
	#read sequences
	seqs_dic = read_seqs(file_type, align_path)
	
	#read partitions file and get genes list
	genes = read_partitions(partition_path)
	
	#add sequences to genes list
	count_seqs(genes, seqs_dic)
		
	#write output
	write_output(genes, align_path)
	
	
				

			
			
			
	
	