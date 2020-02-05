import re
import os
import sys
import pylab
from Bio import SeqIO
import matplotlib.pyplot as plt

def get_foramt(path):
	with open(path, 'r') as f:
		line = f.readline()
	if ">" in line: 
		return "fasta"
	return "phylip" 

def create_histogram(seqs_file):
	
	#get file name
	file_name = os.path.basename(seqs_file)
	gene_name = file_name.split(".")[0]
	
	records = list(SeqIO.parse(seqs_file, get_foramt(seqs_file)))
	
	#sequences = [record.seq.ungap("-") for record in records]
	
	#remove all characters which are not ACTG
	records_string = [str(record.seq) for record in records]
	sequences = [re.sub( r'([^ACTGactg])', '', sequence) 
			for sequence in records_string]
	
	#sequences lengths
	lengths = [len(sequence) for sequence in sequences]
	
	pylab.hist(lengths, bins=20)
	
	title = "{gene}   {num_sequences} sequences\nLengths {min} to {max}"\
			.format(gene = gene_name,
					num_sequences = len(lengths),
					min = min(lengths),
					max = max(lengths))
	
	pylab.title(title)
	pylab.xlabel("Sequence length (bp)")
	pylab.ylabel("Count")
	pylab.savefig(gene_name + ".png")
	
	
if __name__ == "__main__":

	if len(sys.argv) < 2:
		print "please insert argument"
		sys.exit(0)
	
	seqs_file = sys.argv[1]
	
	create_histogram(seqs_file)