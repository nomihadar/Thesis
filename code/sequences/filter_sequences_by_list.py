import sys, os
from Bio import SeqIO
import argparse

sys.path.append("/groups/itay_mayrose/nomihadar/code/")

OUTPUT = "filtered.fasta"

def get_foramt(path):
	with open(path, 'r') as f:
		line = f.readline()
	if ">" in line: 
		return "fasta"
	return "phylip"

def write_output_biopython(records, output_name):	
	
	output_handle = open(output_name, "w")
	SeqIO.write(records, output_handle, "fasta")

def write_output(records, output_name):	
	
	with open(output_name, 'w') as outf:
		for record in records:
			id = ">" + record.id + "\n"
			sequence = str(record.seq).replace('\n', '') + '\n'
			outf.write(id)
			outf.write(sequence)

def read_list(list_path):

	#get input list_path
	with open(list_path, 'r') as fin:
		list = fin.read().splitlines()
	return list

def filter_sequences(sequences_file, species_list):

	#read sequences - get sequences records
	format = get_foramt(sequences_file)
	sequences_records = list(SeqIO.parse(sequences_file, format))
	
	filtered = [record for record in sequences_records 
				if record.id in species_list]
	
	with open("filter_sequences_logfile", 'w') as f:
		f.write("Sequences path:\n" + sequences_file + "\n")
		f.write("Number of species before filtering: ")
		f.write(str(len(sequences_records)) + "\n")
		f.write("Number of species after filtering: ")
		f.write(str(len(filtered)))
	
	return filtered
	
def filter(sequences_file, species_file, output_name):

	#read species from file
	species_list = read_list(species_file)

	#filter sequences not found in file 
	filtered = filter_sequences(sequences_file, species_list)

	#write output 
	write_output(filtered, output_name)

def filter_paths(paths_file, species_file, output_name):

	#get input list_path
	with open(paths_file, 'r') as f:
		seq_files = f.read().splitlines()

	for seq_file in seq_files:
		
		dir = os.path.basename(seq_file)
		#os.makedirs(dir)
		#os.chdir(dir)
		
		filter(seq_file, species_file, dir)
		
		#os.chdir("../")	
	
			
if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--seq_file', '-f', required=True,
						help='sequence file')
	parser.add_argument('--list', '-l', required=True,
						help='list of species')
	parser.add_argument('--output', '-o', default = OUTPUT,
						help='output name')
	parser.add_argument('-paths', action='store_true', 
						help='file contains paths')
	args = parser.parse_args()
	
	if args.paths:
		filter_paths(args.seq_file, args.list, args.output)
	else:
		filter(args.seq_file, args.list, args.output)

	
	