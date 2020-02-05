from __future__ import division
import os, sys
import argparse
import numpy as np
import pandas as pd
from Bio import SeqIO

#return gap percent of the columns for each site of the median sequence
#the median sequence is the sequence with the median length 

sys.path.append("/groups/itay_mayrose/nomihadar/code/")

OUTPUT = "gap_percent_output.txt"
		
def get_foramt(path):
	with open(path, 'r') as f:
		line = f.readline()
	if ">" in line: 
		return "fasta"
	return "phylip" 
	   
def main(align, output): #align file

	records = list(SeqIO.parse(align, get_foramt(align)))
	records = sorted(records, key=lambda record: len(record.seq.ungap("-")))
	median_record = records[len(records)//2] #record of sequence with median length
	
	alignment_length = len(records[0].seq) #get alignment length
	num_sequences = len(records)
	
	percents = []
	for i in range(alignment_length):
		
		num_gaps = sum([1 for record in records 
						if record.seq[i] == "-"])#num gaps in column i
		percent = num_gaps/num_sequences
		
		if not median_record.seq[i] == "-":
			percents.append(percent)

	with open("log", 'w') as f:		
		f.write(median_record.name + "\n")
		f.write(str(median_record.seq)+ "\n")
		f.write("length of median sequence: {}\n".format(len(median_record.seq.ungap("-"))))
		f.write("length of percents array: {}".format(len(percents)))
		
	np.savetxt(output, np.array(percents), fmt = '%.2f')
	#print percents		
	#print median_record.name 
	
if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument('--alignment', '-f',
						help='an alignment file')
	#parser.add_argument('-paths', action='store_true',
	#					help='file with paths of alignments')
	parser.add_argument('-o', required=False,
						default=OUTPUT, help='output name')					
	args = parser.parse_args()
	
	main(args.alignment, args.o)

	
	