import sys
import os

def merge_files(paths_list):

	with open (paths_list, 'r') as f:
		paths = f.read().splitlines()
	
	with open("merged", 'w') as f:
	
		for path in paths:
			
			#get the name of the alignment file 
			file_name = os.path.basename(path)
			
			with open(path, 'r') as fin:
				content = fin.read()
				
				f.write(file_name + ":\n")
				f.write(content + "\n******************************\n")
				
	
if __name__ == "__main__":

	if len(sys.argv) < 2:
		print "please insert argument"
		sys.exit(0)
	
	paths_file = sys.argv[1]

	merge_files(paths_file)