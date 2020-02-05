import os
import sys
import argparse

sys.path.append("/groups/itay_mayrose/nomihadar/code/")


def remove_gaps(alignment_path, output):
	
	with open(alignment_path, 'r') as f:
		alignment = f.read()
		new_alignment = alignment.replace("-","")
		
	if not output:
		output = os.path.basename(alignment_path)	
		
	with open(output, 'w') as fout:	
		fout.write(new_alignment)

		
def remove_gaps_paths(paths_file, output):

	#get input list_path
	with open(paths_file, 'r') as f:
		files = f.read().splitlines()
		
	for file in files:
		remove_gaps(file, output_file)

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--alignment_file', '-f', required=True, 
						help='alignment file')
	parser.add_argument('--output', '-o', required=False,
						default="", help='output name')					
	parser.add_argument('-paths', action='store_true', 
						help='file contains paths')
	
	args = parser.parse_args()
	
	if args.paths:
		remove_gaps_paths(args.alignment_file, args.output)
	else:
		remove_gaps(args.alignment_file, args.output)