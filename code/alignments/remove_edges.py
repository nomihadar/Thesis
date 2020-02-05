from __future__ import division
#remove edges as in the input alignment
import re
import os, sys
import argparse
from Bio import SeqIO

sys.path.append("/groups/itay_mayrose/nomihadar/code/")

from alignments import get_foramt as gf 

OUTPUT_FORMAT = "fasta"

	
def get_records(path):
	return list(SeqIO.parse(path, gf.get_foramt(path)))
	
def remove_edges(path, msa_dic):
	
	records = get_records(path)
	
	sequences = []
	for record in records:
	
		seq = str(record.seq)
		ref_seq = msa_dic[record.id]
		
		regex = re.search("(-*).*?(-*$)", ref_seq)
		start_edge = len(regex.group(1))
		end_edge = len(regex.group(2))
		
		#length percentage
		start = int((start_edge / len(ref_seq)) * len(seq))
		end = int((end_edge / len(ref_seq)) * len(seq))
		
		seq = seq[start:]
		if end:
			seq = seq[:-end]

		sequences.append([record.id, seq])

	return sequences
	
def write_output(seq_file, output):
	with open(output, 'w') as f:
		for seq in seq_file:
			sequence_line = ">{}\n{}\n".format(seq[0], seq[1]) 
			f.write(sequence_line)
	
def main_paths(paths_file, msa_file):
	
	with open(paths_file, 'r') as fin:
		files_paths = fin.read().splitlines()
		
	msa_records = get_records(msa_file)
	msa_dic = {record.id : str(record.seq) for record in msa_records}
	
	for path in files_paths:
		file_name = os.path.basename(path)
		seq_file = remove_edges(path, msa_dic)	
		write_output(seq_file, file_name)
		
def main(seq_file, msa_file):
	
	msa_records = get_records(msa_file)
	msa_dic = {record.id : str(record.seq) for record in msa_records}
	
	file_name = os.path.basename(seq_file)
	seq_file = remove_edges(seq_file, msa_dic)	
	write_output(seq_file, file_name)		
		
		
if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--seq_file', '-s', required=True,
						help='sequences file ')
	parser.add_argument('--msa_file', '-m', required=True,
						help='alignment file with same species')
	parser.add_argument('-paths', action='store_true',
						help="sequences file is file with paths of sequences")
	args = parser.parse_args()

	if args.paths:
		main_paths(args.seq_file, args.msa_file)
	else:
		main(args.seq_file, args.msa_file)
			