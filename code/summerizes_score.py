import sys
import csv
import numpy as np


def read_files(paths_file):
	
	arr_ls = []
	
	with open (paths_file, 'r') as fin:
		lines = fin.read().splitlines()
	
	for line in lines:
	
		splited = line.split(',')
		tree_id = int(splited[0])
		path = splited[1]
		
		arr = np.genfromtxt(path, dtype=float, delimiter=',', skip_header = 1)
		arr = np.insert(arr, 0, tree_id, axis=1)
		
		arr_ls.append(arr)
		
	return arr_ls

def merge_tables(arr_ls):

	max_lines = max([arr.shape[0] for arr in arr_ls])

	merged = []
	for i in range(max_lines):
		for arr in arr_ls:
			if i < arr.shape[0]:
				merged.append(arr[i,:])
			
	array = np.asarray(merged)
	return array

def write_output(big_table):	
	
	# titles = ["tree id", "group size minimal", "num groups", 
				# "score1 average", "score1 median",
				# "score2 average","score2 median",
				# "num monophyly"]
				
	titles = ["tree id", "group size minimal", "num groups", 
				"score1 average", 
				"score2 average",
				"% monophyly"]
	
	ids = set(big_table[:,0])
	ids_str = '_'.join(str(int(x)) for x in ids)

	out_name = "compare_{}.csv".format(ids_str)
	
	with open(out_name, 'w') as fout:
		cas_handle = csv.writer(fout, delimiter = ',')
		cas_handle.writerow(titles)
		cas_handle.writerows(big_table)
		

if __name__ == "__main__":

	if len(sys.argv) < 2:
		print "please insert argument"
		sys.exit(0)
	
	paths_file = sys.argv[1]
	
	arr_ls = read_files(paths_file)

	big_table = merge_tables(arr_ls)
	
	write_output(big_table)
		
		
	
	