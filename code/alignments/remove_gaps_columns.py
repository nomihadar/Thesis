import sys
import os
import numpy as np
from Bio import AlignIO 
from subprocess import call
import time

TEMP_FILE = 'concat_temp'
LOG_FILE = 'concat_logfile'
PARTITIONS_FILE = 'concat_partitions'

class Align:
	def __init__(self, file_name, species, sequences, length):
		self.file_name = file_name
		self.species = species
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
		species = [record.id for record in align_object]
		sequences = [str(record.seq).upper() for record in align_object]
		
		#sequences = {record.id: str(record.seq).upper() for record in align_object}
		
		#create my alignment object 
		align = Align(file_name, sequences, len(align_object[0].seq))
		
		alignments.append(align)
		
	return alignments

def write_concatenated(alignment, final_name = FINAL_FILE):
	 
	#alignment with question mark
	temp_align = ''
	for id, seq in alignment.iteritems():
		temp_align += '>' + id + "\n" + seq + "\n"

	#alignment without question mark
	final_align = temp_align.replace('?', '-')
		
	with open(final_name, 'w') as f:
		f.write(final_align)
	
def	convert_to_phylip():

	while os.path.isfile(FINAL_FILE) and os.stat(FINAL_FILE).st_size == 0:
		pass
			
	convert(FINAL_FILE, "concat.phylip", "fasta", "phylip")

def main(files_list):

	#read alignments
	alignments = read_alignments(files_list)

	
	
	#write alignments in temp format and final format
	write_concatenated(concat_alignment)


	#write partitions file
	write_partitions_file(alignments)

	#convert to phylip
	convert_to_phylip()

if __name__ == "__main__":

	if len(sys.argv) < 2:
		print "please insert argument"
		sys.exit(0)
	
	#get a path to file of list of paths to MSAs files 
	files_list = sys.argv[1]
	
	main(files_list)
	
	