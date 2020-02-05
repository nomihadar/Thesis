import os, sys
import re, argparse
from subprocess import call

sys.path.append("/groups/itay_mayrose/nomihadar/code/")

import run_job as rj

MAX_ITERATE = 1000
OUTPUT = "mafft_{gene}.fasta"

#module load mafft/mafft7310
MODULE = "module load mafft/mafft7149"

#default option 
MAFFT_CMD = "mafft --maxiterate {max_iter} {input} > {output}"
#fast option 
MAFFT_CMD = "mafft {input} > {output}"
#auto option 
MAFFT_CMD = "mafft --amino --auto --maxiterate {max_iter} {input} > {output}"

def run_mafft(seq_file, output):
	#fit indel parameters
	cmd = MAFFT_CMD.format(max_iter = MAX_ITERATE,
							input = seq_file, 
							output = OUTPUT)
	
	#rj.run_job(cmd, "job_mafft.sh")
	#call(MODULE.split(" "))
	call(cmd.split(" "))
	
def run_mafft_paths(paths_file, output):

	#get input list_path
	with open(paths_file, 'r') as f:
		paths = f.read().splitlines()

	for path in paths:
		dir = os.path.basename(path)
		os.makedirs(dir)
		os.chdir(dir)
		
		gene = dir.split(".")[0]
		output = OUTPUT.format(gene = gene)
		
		run_mafft(path, output)
		
		os.chdir("../")
	
if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--seq_file', '-s', required=True, 
						help='sequence file')
	parser.add_argument('--output', '-o', required=False, help='output name')					
	parser.add_argument('-paths', action='store_true', 
						help='file contains paths')
	args = parser.parse_args()
	
	if args.paths:
		run_mafft_paths(args.seq_file, args.output)
	else:
		run_mafft(args.seq_file, args.output)
		
