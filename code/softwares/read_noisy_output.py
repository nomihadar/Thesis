import os, sys
import argparse, re
import pandas as pd
from subprocess import call

sys.path.append("/groups/itay_mayrose/nomihadar/code/")

NOISY_OUTPUT = ".gr"
OUTPUT = "noisy_results.csv"
OUTPUT_MEANS = "noisy_results_means.csv"

def read_indels(path):

	with open(path, 'r') as f:
		content = f.read()
		
	reg = '# statistic:.*len (\d+) red (\d+) RP (\d+\.\d+)'	
	result = re.search(reg, content)
		
	len = int(result.group(1))
	red = int(result.group(2))
	RP = float(result.group(3))
		
	columns = ['len', 'red', 'RP']
	data = [[len, red, RP]]
	df = pd.DataFrame(data, columns=columns, index=[path])			
	
	return df

def main(file, is_paths=False):	
	
	if is_paths:
		with open(file, 'r') as f:
			paths = f.read().splitlines()
		df = [read_indels(path) for path in paths]
		df = pd.concat(df)
		
		#compute means
		print df
		means = {column: [df[column].mean()] for column in df}
		means['# scores'] = len(df)
		means = pd.DataFrame(means)
		means.to_csv(OUTPUT_MEANS, index=False)
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

	