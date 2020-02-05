import os, sys
import argparse, re
import pandas as pd
from subprocess import call

sys.path.append("/groups/itay_mayrose/nomihadar/code/")

import run_job

NOISY_CMD = 'module load gcc\n"/groups/itay_mayrose/nomihadar/softwares/noisy/Noisy-1.5.12/noisy" {fasta_file}'

def run_noisy(fasta_file):
	cmd = NOISY_CMD.format(fasta_file=fasta_file)
	run_job.run_job(cmd, "job_run_noisy.sh")

def run_noisy_paths(fasta_file):
	
	#get input list_path
	with open(fasta_file, 'r') as f:
		paths = f.read().splitlines()

	for path in paths:
		dir = os.path.basename(path)
		os.makedirs(dir)
		os.chdir(dir)
		
		run_noisy(path)
		
		os.chdir("../")
	
if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--fasta_file', '-f', required=True,
						help='path of alignment file')
	parser.add_argument('-paths', action='store_true', 
						help='file contains paths')
	args = parser.parse_args()
	
	if args.paths:
		run_noisy_paths(args.fasta_file)
	else:
		run_noisy(args.fasta_file)

	