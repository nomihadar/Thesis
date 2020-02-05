import os, sys
import argparse
from Bio import SeqIO

sys.path.append("/groups/itay_mayrose/nomihadar/code/")

from alignments import get_foramt as gf 

OUTPUT_FORMAT = "fasta"

class Sequences(object):
	
	#key = species, value = genes  
	species_dic = {}
	all_species_incover = []
	
	def __init__(self, gene_name, sequences_records):
		self.gene_name = gene_name
		self.sequences = sequences_records
		self.species = []
		self.sequences_in_cover = []
		self.species_in_cover = []
	
		self.set_species()
	
	def get_num_seqs(self):
		return len(self.sequences)
	
	def get_num_seqs_incover(self):
		return len(self.sequences_in_cover)
	
	def set_species(self):
		self.species = [record.id for record in self.sequences]
	
	def set_species_in_cover(self):
		self.species_in_cover = [record.id for record in self.sequences_in_cover]


def read_seuences(paths_file):

	with open(paths_file, 'r') as fin:
		files_paths = fin.read().splitlines()

	sequences = []
	for path in files_paths:
		
		#get file name
		file_name = os.path.basename(path)
		
		gene_name = file_name.split(".")[0]
		
		#get sequences records
		sequences_records = list(SeqIO.parse(path, gf.get_foramt(path)))
		
		#create a sequences object 
		sequences_obj = Sequences(gene_name, sequences_records)
		
		#set dictionary 
		for species in sequences_obj.species:
			if species in Sequences.species_dic:
				Sequences.species_dic[species].append(gene_name)
			else:
				Sequences.species_dic[species] = [gene_name]
		
		#add to list 
		sequences.append(sequences_obj)
	
	return sequences
	
def filter_by_cover(sequences_list, min_genes):

	all_species_incover = []
	for seqs_obj in sequences_list:
		sequences_incover = [sequence for sequence in seqs_obj.sequences
							if len(Sequences.species_dic[sequence.id]) 
								>= min_genes]
		seqs_obj.sequences_in_cover = sequences_incover
		seqs_obj.set_species_in_cover()
		
		all_species_incover.extend(seqs_obj.species_in_cover)

	Sequences.all_species_incover = set(all_species_incover)

def write_output(sequences_list, min_genes, gaps):
	
	for sequences_obj in sequences_list:
		output_name = sequences_obj.gene_name + "." + OUTPUT_FORMAT
		with open(output_name, 'w') as f:
			for seq_record in sequences_obj.sequences_in_cover:
				sequence = str(seq_record.seq).replace("\n", "")
				#remove_gaps
				if not gaps:
					sequence = sequence.replace("-", "")
				sequence_line = ">{}\n{}\n".format(seq_record.id, sequence) 
				f.write(sequence_line)
	
def write_logfile(sequences_list):
	
	logfile = "filter_by_cover_logfile"
	
	with open(logfile, 'w') as f:
		
		sum = "num species in cover: {}\n\n"\
			.format(len(Sequences.all_species_incover))
		f.write(sum)
		
		line_format = "{:15}{:15}{:15}\n"
		title = line_format.format("gene", "#_species", "#_species_incover")
		f.write(title)
		for seqs_obj in sequences_list:
			line = line_format.format(seqs_obj.gene_name,len(seqs_obj.species), 
										len(seqs_obj.species_in_cover))
			f.write(line) 
			
		f.write("\n\n" + ("*" * 80) + "\n\n") 
		
		line_format = "{:15}{:30}\n"
		title = line_format.format("species", "genes")
		f.write(title) 
		for species in Sequences.species_dic:
			genes_str = ', '.join(Sequences.species_dic[species])	
			line = line_format.format(species, genes_str)
			f.write(line)

	with open("species_in_cover.ls", 'w') as f:
		list = '\n'.join(Sequences.all_species_incover)
		f.write(list)

def main(paths, num_genes, gaps):

	sequences_list = read_seuences(paths)

	filter_by_cover(sequences_list, num_genes)
	
	write_output(sequences_list, num_genes, gaps)
	
	write_logfile(sequences_list)
		
if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--paths', '-p', required=True,
						help='file with paths of alignments')
	parser.add_argument('--num_genes', '-n', required=True, type=int,
						help='num genes in cover')
	parser.add_argument('--gaps', '-g', action='store_true', 
						help='with gaps')
	args = parser.parse_args()

	main(args.paths, args.num_genes, args.gaps)
			