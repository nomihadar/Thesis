import sys

sys.path.append("/groups/itay_mayrose/nomihadar/code/")

def get_foramt(path):
	with open(path, 'r') as f:
		line = f.readline()
	if ">" in line: 
		return "fasta"
	return "phylip"