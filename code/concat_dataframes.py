import os, sys
import argparse
import pandas as pd

sys.path.append("/groups/itay_mayrose/nomihadar/code/")

import create_paths_list as create_paths
		
OUTPUT = 'concatenated_tables.csv'		
OUTPUT_MEANS = 'concatenated_tables_means.csv'	
def main(paths_file, output, output2, mean):	

	#get input list_path
	with open(paths_file, 'r') as f:
		files = f.read().splitlines()
	
	frames = []
	for file in files:
		frame = pd.read_csv(file)
		frame['file'] = [file] * len(frame)
		#frame.index = [os.path.dirname(file)] 
		frames.append(frame)
		
	final = pd.concat(frames)
	final.to_csv(output, index=False)
	
	#compute means
	if mean:
		d = {}
		for column in final.iloc[:,:-1]:
			d[column + " std"] = [final[column].std()]
			d[column + " avg"] = [final[column].mean()]
			
		df = pd.DataFrame(d)
		df.to_csv(output2, index=False)
	
if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--paths_file', '-f', required=True,
						help='files contains paths to concat')
	parser.add_argument('--output', '-o', required=False,
						default=OUTPUT, help='output name')
	parser.add_argument('--output2', '-o2', required=False,
						default=OUTPUT_MEANS, help='output name')
	parser.add_argument('-root', action='store_true', 
						help='root contains sequences file')
	parser.add_argument('--suffix', '-s', required=False,
						help='suffix, comes with the root argument')
	parser.add_argument('-mean', action='store_true', 
						help='compute mean')
	args = parser.parse_args()

	if args.root:
		create_paths.main(args.paths_file, args.suffix)
		
		main("paths.txt", args.output, args.output2, args.mean)
	else:
		main(args.paths_file, args.output, args.output2, args.mean)
		
		
		
		
		
	