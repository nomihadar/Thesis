import os, sys
import re, argparse
import numpy as np
from subprocess import call
from Bio import AlignIO 
import pandas as pd
from scipy.stats import chisquare

sys.path.append("/groups/itay_mayrose/nomihadar/code/")

import run_job as rj
from alignments import count_unique_gaps 


BLOCK_NAME = "block_{}.fas"
COUNTS = "block_{}_counts.txt"

def get_foramt(path):
	with open(path, 'r') as f:
		line = f.readline()
	if ">" in line: 
		return "fasta"
	return "phylip" 
	
def create_block(align_object, start, end, num_block):
	
	sequences = []
	for record in align_object:
		sequence = str(record.seq)
		new_seq = [record.id, sequence[start:end]]
		sequences.append(new_seq)
	
	with open(BLOCK_NAME.format(num_block) , 'w') as f:
		for seq in sequences:
			f.write(">{}\n{}\n".format(seq[0],seq[1]))
		
	
def main(msa_file, num_blocks, edges, output):
	
	#create blocks file 
	align_object = AlignIO.read(open(msa_file), get_foramt(msa_file))
	msa_length = len(align_object[0].seq)
	len_block = msa_length / num_blocks
	
	start, end = (0,0)
	for num_block in range(1,num_blocks+1):
		start = end
		if num_block == num_blocks:
			end = msa_length
		else:
			end = end + len_block
		create_block(align_object, start, end, num_block)
	
	#count unique indels in each block
	observations = []
	for num_block in range(1,num_blocks+1):
		file = os.path.join(os.getcwd(), BLOCK_NAME.format(num_block))
		dir = "block_{}".format(num_block)
		os.makedirs(dir)
		os.chdir(dir)
		counts_file = COUNTS.format(num_block) 
		
		count_unique_gaps.main(file, edges, counts_file)
		
		obs = np.loadtxt(counts_file, 'int', ndmin=1)
		observations.append(len(obs))
		os.chdir("../")	
	
	#compute chi-square for goodness of fit  	
	chisq , p = chisquare(observations)
	results = {"chisq": [chisq], "p-value": [p]}
	results = pd.DataFrame(results)
	results.to_csv(output, sep=',', index=False)
	
	np.savetxt("observations.txt", observations)
		
if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--msa_file', '-m', required=True, 
						help='alignment file')
	parser.add_argument('--num_blocks', '-n', required=True, 
						help='number of block', type=int)
	parser.add_argument('-edges', action='store_false',
						help='if specified do not include edges')
	parser.add_argument('--output', '-o', required=False,
						help='output name')					
	args = parser.parse_args()
	
	
	main(args.msa_file, args.num_blocks, args.edges, args.output)

		
