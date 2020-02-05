
import sys
from Bio import SeqIO

def get_foramt(path):
	with open(path, 'r') as f:
		line = f.readline()
	if ">" in line: 
		return "fasta"
	return "phylip"

def get_sequences_species(seqs_file):

	# Load alignment 
	records = list(SeqIO.parse(seqs_file, "phylip"))
		
	# get all species in tree
	species_list = [record.id for record in records]
	
	return species_list
	
def write_output(species_list, output_name):
	
	list_str = '\n'.join(species_list)
	
	with open(output_name, 'w') as fout:
		fout.write(list_str)
	
if __name__ == "__main__":

	if len(sys.argv) < 3:
		print "please insert arguments"
		sys.exit(0)
	
	#get path to tree file
	seqs_file = sys.argv[1]
	
	#get output name
	output_name = sys.argv[2]
	
	species_list = get_sequences_species(seqs_file)
	
	print "# sequences:", len(species_list)
	
	write_output(species_list, output_name)	
	