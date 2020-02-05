from __future__ import division
#remove edges as in the input alignment
import re
import os, sys
import argparse
import pandas as pd
import numpy as np
from Bio import SeqIO

sys.path.append("/groups/itay_mayrose/nomihadar/code/")

from alignments import get_foramt as gf 

OUTPUT_FORMAT = "fasta"
KEY1 = '1_%_seqs_with_edges'
KEY2 = '2length_AVG'
KEY3 = '3length_median'
KEY4 = '4length_VAR'
	
KEY5 = '1_AVG_indels_number'	
KEY6 = '2_AVG_indels_lengths'	
KEY7 = '3_VAR_indels_lengths'	
	
def get_records(path):
	return list(SeqIO.parse(path, gf.get_foramt(path)))
	
def compute_statistics_edges(lengths, num_seqs, output):
	
	d = {}
	d[KEY1] = [len(lengths) / num_seqs * 100]
	d[KEY2] = [np.average(lengths)]
	d[KEY3] = [np.median(lengths)]
	d[KEY4] = [np.var(lengths)]
	
	df = pd.DataFrame(d)
	df.to_csv(output, sep=',', index=False)
	
def compute_statistics_middle(lengths, num_seqs, output):
	
	d = {}
	d[KEY5] = [len(lengths) / num_seqs]
	d[KEY6] = [np.average(lengths)]
	d[KEY7] = [np.var(lengths)]
	
	df = pd.DataFrame(d)
	df.to_csv(output, sep=',', index=False)	
	
def edges_indels(path):
	records = get_records(path)
	start_lengths = []
	end_lengths = []
	middle_lengths = []
	for record in records:
		seq = str(record.seq)
		
		regex = re.search("(-*)(.*?)(-*$)", seq)
		start_edge = len(regex.group(1))
		end_edge = len(regex.group(3))
		
		start_lengths.append(start_edge)
		end_lengths.append(end_edge)
		
		middle = regex.group(2)
		gaps = re.findall(r'(-+)', middle)
		middle_lengths.extend([len(gap) for gap in gaps])
		
	compute_statistics_edges(start_lengths, len(records), "start_edges_indels.csv")	
	compute_statistics_edges(end_lengths, len(records), "end_edges_indels.csv")	
	compute_statistics_middle(middle_lengths, len(records), "middle_edges_indels.csv")
	
def internal_inels():

	#set average num gaps	
		num_gaps = [len(re.findall(r'(-+)', str(record.seq)))
						for record in records]
		self.average_num_gaps = np.average(num_gaps)
	
		# set average gaps length
		gaps_lengths = []
		for record in records:
			gaps = re.findall(r'(-+)', str(record.seq))
			gaps_lengths.extend([len(gap) for gap in gaps])
		if not gaps_lengths:
			gaps_lengths = 0
		self.average_gaps_length = np.average(gaps_lengths)	
	
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
		
def main(msa_file):
	
	edges_indels(msa_file)	
		
		
if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--msa_file', '-m', required=True,
						help='alignment file with same species')
	parser.add_argument('-paths', action='store_true',
						help="sequences file is file with paths of sequences")
	args = parser.parse_args()

	if args.paths:
		main_paths(args.seq_file, args.msa_file)
	else:
		main(args.msa_file)
			