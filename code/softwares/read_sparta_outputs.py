import os, sys
import argparse, re
import pandas as pd
from subprocess import call

sys.path.append("/groups/itay_mayrose/nomihadar/code/")

SPARTA_OUTPUT = "bestResult.txt"
OUTPUT = "chosen_indels.csv"

def read_indels(path):

	#guidance_output_dir
	with open(path, 'r') as f:
		indels = f.read().splitlines()
		indels = indels[0].split()
		
	ir = indels[2]
	a = indels[3]
	rl = indels[4]
		
	columns = ['ir', 'a', 'rl']
	data = [[ir, a, rl]]
	df = pd.DataFrame(data, columns=columns, index=[path])			
	
	return df

def main(file, is_paths=False):	
	
	if is_paths:
		with open(file, 'r') as f:
			paths = f.read().splitlines()
		df = [read_indels(path) for path in paths]
		df = pd.concat(df)
	else:
		df = read_indels(file)
			
	df.to_csv(OUTPUT)
	
if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--file', '-f', required=False,
						help='best results file')
	parser.add_argument('-paths', action='store_true',
						help='file cntains files paths')
	args = parser.parse_args()
	
	main(args.file, args.paths)

	