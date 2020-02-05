import os
import sys
import numpy as np
import argparse
from subprocess import call
	
TRIMAL_CMD = '/share/apps/trimAl/trimal -in {align} -out {output} -phylip -gt {gapthreshold}'

GAP_THRESHOLD = 0.8
	
def trimal(align, output, gapthreshold = GAP_THRESHOLD):

	#create the arguments file for qsub 
	trimal_cmd = TRIMAL_CMD.format(align = align, output = output, 
									gapthreshold = gapthreshold)
	
	#run trimal
	call(trimal_cmd.split(" "))		
	
def trimal_multiply(paths_list):
		
	with open (paths_list, 'r') as f:
		paths = f.read().splitlines()

	for path in paths:	
		
		output = os.path.basename(path)
		
		run_trimal(align, output, GAP_THRESHOLD)

		
if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='')

	parser.add_argument('--paths_list', '-paths', required=True,
						help='file of alignments paths')
	
	'''	
	parser.add_argument('--output', '-out', required=True,
						, help='tree2 file')
						
	parser.add_argument('--output', '-out', required=True,
						, help='tree2 file')
						'''
	
	args = parser.parse_args()
	paths_list = args.paths_list

	main(paths_list)