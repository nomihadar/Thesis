from __future__ import division 
import os, sys
import argparse, logging
import time, math
from subprocess import call
from Bio import SeqIO 
from ete3 import Tree

sys.path.append("/groups/itay_mayrose/nomihadar/code/")

import mylogger 
import run_indelible
from alignments import convert_formats 
import get_indel_parameters as indel

DIR_NAME = 'block_{}'
#INDEL_PARAMS_METHOD ="distribution","constant", "block_optimized"
REFERENCE_DIR = "reference_blocks"
REF_FILE = 'block_{}.fas'
INDEL_DIR = "indels_files"
INDEL_FILE = "chosen_indels.csv"
BLOCKS_DIR = "blocks_simulations"
	
#block 
class Block:
	def __init__(self, block_id, seqs, seqs_aligned):
		self.block_id = block_id 
		self.seqs = seqs #dict {species : sequence}
		self.seqs_aligned = seqs_aligned #dict {species : aligned sequence}
	
	#species list - to save the species order 
	def write(self, species_list, output_name):
		write(self.seqs_aligned, species_list, output_name)
			
#file of simulated seqs 		
class SimFile:
	def __init__(self, sim_id, blocks):
		self.sim_id = sim_id
		self.blocks = blocks
		self.concat_seqs = {}
		self.concat_seqs_aligned = {}
		
		self.concatenate_seqs()
		
	def concatenate_seqs(self):
	
		species_list = self.blocks[0].seqs.keys()
	
		for species in species_list:
			seq = ''
			seq_aligned = ''
			for block in self.blocks:	
				seq += block.seqs[species]
				seq_aligned += block.seqs_aligned[species]
			
			self.concat_seqs[species] = seq
			self.concat_seqs_aligned[species] = seq_aligned

	def write_seqs(self, species_list, output_name):
		write(self.concat_seqs, species_list, output_name)
		
	def write_aligned(self, species_list, output_name):
		write(self.concat_seqs_aligned, species_list, output_name)

def get_foramt(path):
	with open(path, 'r') as f:
		line = f.readline()
	if ">" in line: 
		return "fasta"
	return "phylip" 
		
def write(seqs, species_list, output_name):
	file = ''
	for species in species_list:
		seq = seqs[species]
		file += '>{}\n{}\n'.format(species, seq) 
	with open(output_name, 'w') as f:
		f.write(file)
		
#split a mas to blocks 
def split_to_blocks(msa, num_blocks, species_list):
	#reas msa
	seq_object = SeqIO.parse(open(msa), get_foramt(msa))
	sequences = {record.id : str(record.seq).upper() 
						for record in seq_object}
	
	alignment_length = len(sequences.itervalues().next()) 
	block_length = int(math.ceil(alignment_length / num_blocks))

	blocks = [] 
	loc = 0 #location
	for block_id in range(1,num_blocks+1):
		seqs_alined = {species: seqs[loc:loc+block_length]
					for species, seqs in sequences.iteritems()} 
		#create block file 
		block = Block(block_id, {}, seqs_alined)
		blocks.append(block)
	
		loc += block_length
		
	logging.info("block length: {}".format(block_length))

	#write blocks to files
	os.makedirs(REFERENCE_DIR)
	os.chdir(REFERENCE_DIR)
	for block in blocks:
		output_name = REF_FILE.format(block.block_id)
		block.write(species_list, output_name)
	os.chdir("../")		
	
def read_seq_file(path):
	#read files
	while not os.path.isfile(path):
		time.sleep(5)
	seq_object = SeqIO.parse(open(path), get_foramt(path))
	sequences = {record.id : str(record.seq).upper() 
						for record in seq_object}
	return sequences
	
def read_blocks(gene, sim_id, num_blocks):

	blocks = []
	for block_id in range(1,num_blocks+1):
		
		#paths
		dir_name = DIR_NAME.format(block_id)
		
		block_file = "{}_{}.fas".format(gene, sim_id)
		block_file_aligned = "{}_TRUE_{}.phy".format(gene, sim_id)
	
		path = os.path.join(BLOCKS_DIR, dir_name, block_file)
		path_alined = os.path.join(BLOCKS_DIR, dir_name, block_file_aligned)
			
		seqs = read_seq_file(path)
		seqs_alined = read_seq_file(path_alined)
				
		#create block file 
		block = Block(block_id, seqs, seqs_alined)
		blocks.append(block)
			
	return blocks
	
#create a file with indel parameters
def simulate_seqs(gene, model_file, tree_file, 
					num_blocks, num_simulations, root):
	
	os.makedirs(BLOCKS_DIR)
	os.chdir(BLOCKS_DIR)
	
	for i in range(1,num_blocks+1):
		logging.info("run indelible - block {}".format(i))
		
		dir_name = DIR_NAME.format(i)
		os.makedirs(dir_name)
		os.chdir(dir_name)
		
		indel_file = os.path.join(root, INDEL_DIR, dir_name, INDEL_FILE)
		while not os.path.isfile(indel_file):
			time.sleep(5)
		run_indelible.main(gene, model_file, tree_file, 
							indel_file, num_simulations)
		os.chdir("../")	
	
	os.chdir("../")
	
def get_species(tree_file):	
	tree = Tree(tree_file)
	return [leaf.name for leaf in tree]	
	
def write_file(gene, sim_file, species_list):
					
	output_name = "{}_{}.fas".format(gene, sim_file.sim_id)
	sim_file.write_seqs(species_list, output_name)

	output_name = "{}_TRUE_{}.fas".format(gene, sim_file.sim_id)
	sim_file.write_aligned(species_list, output_name)

	#convert_formats.convert(FINAL_FILE, "concat.phylip", 
	#						"fasta", "phylip")

def create_indel_files(gene, method, model_file, tree_file, indel_file,
						num_simulations, num_blocks, root):
	
	os.makedirs(INDEL_DIR)
	os.chdir(INDEL_DIR)
	
	for block_id in range(1,num_blocks+1):
		
		logging.info("creation of indel file of bock {}".format(block_id))
	
		dir_name = DIR_NAME.format(block_id)
		os.makedirs(dir_name)
		os.chdir(dir_name)
		
		reference = os.path.join(root, REFERENCE_DIR, 
								REF_FILE.format(block_id))
		#create a file with indel parameters
		indel.get_indel_params(gene, model_file, tree_file, indel_file, 
								num_simulations, reference, method)
		
		os.chdir("../")	
	
	os.chdir("../")				
	
def main(gene, method, model_file, tree_file, indel_file, reference, 
			num_blocks, num_simulations, nn):
	
	root = os.getcwd()
	
	#get species - to keep order of species in all MSAs
	species_list = get_species(tree_file)
	
	#split reference alignment into blocks 
	split_to_blocks(reference, num_blocks, species_list)
	
	logging.info("reference msa was splited to blocks")
	
	#create indel files
	create_indel_files(gene, method, model_file, tree_file, indel_file,
						nn, num_blocks, root)
	
	logging.info("creation of indel files")
	
	#simulate sequences
	simulate_seqs(gene, model_file, tree_file, 
					num_blocks, num_simulations, root)
	
	logging.info("collect blocks to files")
	
	#concatenate blocks to one files  
	for sim_id in range(1,num_simulations+1):	
		
		#concat sequences of simulation id
		blocks = read_blocks(gene, sim_id, num_blocks)
		sim_file = SimFile(sim_id, blocks)
		write_file(gene, sim_file, species_list)
		
	logging.info("done")
	
	#delete temp files
	
	
if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='')
	
	parser.add_argument('--gene', '-g', required=True,
						 help='name of gene')
	parser.add_argument('-method', required=True,
						 help='indel inference parameter method')
	parser.add_argument('--tree_file', '-t', required=True,
						 help='path to tree')
	parser.add_argument('--model_file', '-m', required=True,
						 help='path to tree')
	parser.add_argument('-indel', required=False, default ='',
						 help='path to indel model - in case of constant')
	parser.add_argument('--reference', '-r', required=True,
						help='path to refernce alignment')
	parser.add_argument('--num_blocks', '-b', required=True, type=int,
						help='number of blocks')				
	parser.add_argument('--num_simulations', '-n', required=True, type=int,
						help='number of simulations')
	parser.add_argument('-nn', required=True, type=int,
						help='number of simulations for fitting indels')
	args = parser.parse_args()
	
	mylogger.initialize("indelible_on_blocks.logfile")
	logging.info("gene name: {}".format(args.gene))
	logging.info("indel inference parameter method: {}".format(args.method))
	logging.info("tree file:, {}".format(args.tree_file))
	logging.info("model file:, {}".format(args.model_file))
	logging.info("indel file:, {}".format(args.indel))
	logging.info("reference file:, {}".format(args.reference))
	logging.info("numbers of block:, {}".format(args.num_blocks))
	logging.info("numbers of simulations: {}".format(args.num_simulations))
	logging.info("numbers of simulations for fitting indels: {}".format(args.nn))
	
	main(args.gene, args.method, args.model_file, args.tree_file, args.indel,
		args.reference, args.num_blocks, args.num_simulations, args.nn)	
		