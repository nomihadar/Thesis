import os, sys
import argparse
import numpy as np
import pandas as pd

sys.path.append("/groups/itay_mayrose/nomihadar/code/")

def read(path):
	data = np.loadtxt(path, 'int', ndmin=1)
	return data

def get_observations(files, concat):
	if not concat:
		observations = read(files)
	else:
		with open(files, 'r') as f:
			paths = f.read().splitlines()
		observations = []
		for path in paths:
			obs = read(path)
			observations.extend(obs)			
	return observations			
	
def main(observations_file, concat, output):

	observations = get_observations(observations_file, concat)
	
	occurrences = np.bincount(observations)
	
	#save as an histogram 
	d = {"occurrences": occurrences[1:], 
		"lengths": range(1,max(observations)+1)}
	df = pd.DataFrame(d)
	df.to_csv(output, sep=',', index=False)	
		
	#save all observations in one file 	
	np.savetxt("observations.txt", observations, '%d')	
		
	
if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--observations_file', '-f', required=True, 
						help='alignment file')
	parser.add_argument('--output', '-o', required=False,
						default="plot.png",help='output name')
	parser.add_argument('-concat', action='store_true',
						help=" observed taken from several files")						

	args = parser.parse_args()
	
	main(args.observations_file, args.concat, args.output)
