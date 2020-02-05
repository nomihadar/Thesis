import sys
from Bio import AlignIO

def get_foramt(path):
	with open(path, 'r') as f:
		line = f.readline()
	if ">" in line: 
		return "fasta"
	return "phylip" 


def get_min_max_boundaries_from_msa(align_path):

	# Load alignment 
	records = AlignIO.read(open(align_path), get_foramt(align_path))
	
	sizes = [len(record.seq.ungap("-")) for record in records]

	min_len = 0.9 * min(sizes) 
	max_len = 1.1 * max(sizes)
	
	return (int(min_len), int(max_len))

if __name__ == "__main__":

	if len(sys.argv) < 2:
		print "please insert arguments"
		sys.exit(0)
	
	#get path to tree file
	align_path = sys.argv[1]
	
	(min_len, max_len) = get_min_max_boundaries_from_msa(align_path)
	
	print "min length: ", min_len
	print "max length: ", max_len
	