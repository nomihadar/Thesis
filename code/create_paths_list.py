import os, sys
import argparse

sys.path.append("/groups/itay_mayrose/nomihadar/code/")

OUTPUT_FILE = "paths.txt"

def create_list(root, suffix):
	paths = []

	for root, dirs, files in os.walk(root, topdown=True):
		for file in files:
			#if file ends with input suffix - append to the output list 
			if file.endswith(suffix): #and "lengths" in file: #and "TRUE" not in file:	
				paths.append(os.path.join(root, file))	
	return paths
	
def create_list_flat(root, suffix):
	paths = []
	for file in os.listdir(root):
		if file.endswith(suffix) and "TRUE" not in file:	
			paths.append(os.path.join(root, file))	
			
	return paths

def write_output(paths, output_file, size):
	#create a file of files paths
	with open(output_file, "w") as fout:
		sorted_paths = sorted(paths)
		
		if size:
			sorted_paths = sorted_paths[:size]
		
		for path in sorted_paths:
			line = "{}\n".format(path)
			fout.write(line)
	
def main(root, suffix, size=0, output_file=OUTPUT_FILE, flat=False):
	
	if flat:
		paths = create_list_flat(root, suffix)
	else:
		paths = create_list(root, suffix)
	
	write_output(paths, output_file, size)
	
if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--root', '-r', required=True,
						 help='root directory contains desired files')
	parser.add_argument('--suffix', '-s', required=True,
						 help='suffix of desired files')
	parser.add_argument('--output_file', '-o', required=False,
						default= OUTPUT_FILE, help='output file')
	parser.add_argument('-flat', action='store_true',
						help='collect files from first level only')
	parser.add_argument('-size', type=int, default=0,
						help='size of list')
	args = parser.parse_args()

	main(args.root, args.suffix, args.size, args.output_file, args.flat)