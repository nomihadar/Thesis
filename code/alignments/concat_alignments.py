import sys
import os
import argparse
from Bio import AlignIO 
from subprocess import call
from convert_formats import convert

sys.path.append("/groups/itay_mayrose/nomihadar/code/")

FINAL_FILE = 'concat.fasta'
TEMP_FILE = 'concat_temp'
LOG_FILE = 'concat_logfile'
PARTITIONS_FILE = 'concat_partitions'

class Align:
	def __init__(self, file_name, sequences, length):
		self.file_name = file_name
		self.sequences = sequences
		self.length = length
		
	def get_species(self):
		return self.sequences.keys()
		
def get_foramt(path):
	with open(path, 'r') as f:
		line = f.readline()
	if ">" in line: 
		return "fasta"
	return "phylip" 
	   
def read_alignments(paths_list):

	with open (paths_list, 'r') as f:
		paths = f.read().splitlines()
	
	alignments = []	
	for path in paths:
		
		align_object = AlignIO.read(open(path), get_foramt(path))
		
		#get the name of the alignment file 
		file_name = os.path.basename(path)
		#create a dictionary of sequences 
		sequences = {record.id: str(record.seq).upper() 
					for record in align_object}
		
		#create my alignment object 
		align = Align(file_name, sequences, len(align_object[0].seq))
		
		alignments.append(align)
		
	return alignments


def get_partitions(alignments):
	
	partitions = {}
	pos = 1
	for alignment in alignments:
		partitions[alignment.file_name] = (pos, pos + alignment.length-1)
		pos += alignment.length
		
	return partitions
	
def write_concatenated(alignment, temp_name = TEMP_FILE, 
						final_name = FINAL_FILE):
	 
	#alignment with question mark
	temp_align = ''
	for id, seq in alignment.iteritems():
		temp_align += '>' + id + "\n" + seq + "\n"
	
	#with open(temp_name, 'w') as f:
	#	f.write(temp_align)
	
	#alignment without question mark
	final_align = temp_align.replace('?', '-')
		
	with open(final_name, 'w') as f:
		f.write(final_align)

		
def write_partitions_file(alignments, partition_file = PARTITIONS_FILE):

	partitions = get_partitions(alignments)
	
	with open (partition_file , 'w') as f:
		for alignment in alignments:
			(start, end) = partitions[alignment.file_name] 
			line = 'DNA, {0} = {1}-{2}\n'\
						.format(alignment.file_name, start, end)
			f.write(line)
		
def write_logfile(alignments, all_species, logfile_name = LOG_FILE):
	
	#get partitions
	partitions = get_partitions(alignments)
	
	with open (logfile_name , 'w') as f:
		
		title = '{0: <12} {1: <12} {2: <12} {3}\n'\
				.format("species", "start", "end", "gene_name")
		f.write(title)
		
		pos = 0
		for id in all_species:
			for alignment in alignments:
				(start, end) = partitions[alignment.file_name] 
			
				if "?" in alignment.sequences[id]:
					gene_name = "?"
				else:
					gene_name = alignment.file_name
				
				line = '{0: <12} {1: <12} {2: <12} {3}\n'\
						.format(id, start, end, gene_name)
				f.write(line)

def get_all_species(alignments):
	all_species = []
	for alignment in alignments:
		all_species.extend(alignment.get_species())
	return set(all_species)
	
def concat_sequences(alignments, id):
	concatenated = ''
	for alignment in alignments:
		concatenated += alignment.sequences[id] 
	return concatenated
	
def concatenate(alignments, all_species):
	
	#add gaps to species which doesn't have sequences
	for alignment in alignments:
		for id in all_species:
			if id not in alignment.sequences:
				alignment.sequences[id] = '?' * alignment.length	
	
	concat_alignment = {}
	for id in all_species:
		concat_alignment[id] = concat_sequences(alignments, id)
	
	return concat_alignment
 	
def	convert_to_phylip():

	while os.path.isfile(FINAL_FILE) and os.stat(FINAL_FILE).st_size == 0:
		pass
			
	convert(FINAL_FILE, "concat.phylip", "fasta", "phylip")

def concat_alignments(files_list):

	#read alignments
	alignments = read_alignments(files_list)
	
	#get all species in one list 
	all_species = get_all_species(alignments)
	
	#concat alignments
	concat_alignment = concatenate(alignments, all_species)

	#write alignments in temp format and final format
	write_concatenated(concat_alignment)
	
	#write log file 
	write_logfile(alignments, all_species)

	#write partitions file
	write_partitions_file(alignments)

	#convert to phylip
	convert_to_phylip()

if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--paths_file', '-p', required=True,
						help='paths of alignments')
	args = parser.parse_args()

	concat_alignments(args.paths_file)	
	