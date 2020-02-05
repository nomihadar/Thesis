from __future__ import division
import os, sys
import re, argparse
import numpy as np
from subprocess import call
from Bio import SeqIO

sys.path.append("/groups/itay_mayrose/nomihadar/code/")

def get_foramt(path):
	with open(path, 'r') as f:
		line = f.readline()
	if ">" in line: 
		return "fasta"
	return "phylip" 
	
def missing_per_site(msa_file, output):

	records = list(SeqIO.parse(msa_file, get_foramt(msa_file)))
	
	proportion = 0
	numgaps = 0
	for record in records:
		seq = str(record.seq)
		numgaps += seq.count('-')
	
	proportion = numgaps / (len(seq) * len(records))
	
	with open (output, 'w') as f:
		s = "proportion of missing data: {}\n".format(proportion)
		f.write(s)	
	
def main(msa_file, output):

	records = list(SeqIO.parse(msa_file, get_foramt(msa_file)))
	
	proportion = 0
	numgaps = 0
	for record in records:
		seq = str(record.seq)
		numgaps += seq.count('-')
	
	proportion = numgaps / (len(seq) * len(records))
	
	with open (output, 'w') as f:
		s = "proportion of missing data: {}\n".format(proportion)
		f.write(s)
	
if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--msa_file', '-m', required=True, 
						help='alignment file')
	
	parser.add_argument('--output', '-o', required=False,
						default= "missing_data_output.txt", help='output name')					
	args = parser.parse_args()
	
	
	main(args.msa_file, args.output)

		
