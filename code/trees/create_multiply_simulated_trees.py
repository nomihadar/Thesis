#once was called: compare_trees.py
import sys, os, time, argparse, logging

from Bio import AlignIO
from Bio import SeqIO
from subprocess import call

sys.path.append("/groups/itay_mayrose/nomihadar/code/")

import mylogger
from alignments import concat_alignments as ca
from softwares import run_trimal 


INDELIBLE_SEQS_UNALIGNED = "/groups/itay_mayrose/nomihadar/simulations/simulated_sequences/4_genes_cover/indelible_15.04.17/{gene}/{gene}_{i}.fas" 
INDELIBLE_SEQS_ALIGNED = "/groups/itay_mayrose/nomihadar/simulations/simulated_sequences/4_genes_cover/indelible_15.04.17/{gene}/{gene}_TRUE_{i}.phy"

GENES = ['18S', '26S', 'atpB', 'rbcL',  'ITS', 'trnLtrnF', 'matK']

QSUB_ARGS = """#!/bin/tcsh
#$ -N python 
#$ -S /bin/tcsh
#$ -cwd
#$ -l itaym
#$ -p 0
#$ -e $JOB_NAME.$JOB_ID.ER
#$ -o $JOB_NAME.$JOB_ID.OU

module load python/python-2.7.6
module load examl
{cmd}
touch flag_job_is_done
"""

MAFFT_MODULE = "module load mafft/mafft7149\n"
EXAML_CMD = 'python ~/code/trees/run_examl.py -m {align_phylip} -p {partitions} -o {name}'
MAFFT_CMD = "mafft --auto --maxiterate 1000 {input} > gene_{gene}.mafft"

def run_qsub(file_name, cmd):

	#create the arguments file for qsub 
	with open(file_name, 'w') as fout:
		qsub_args = QSUB_ARGS.format(cmd = cmd)
		fout.write(qsub_args)

	#run phlawd on queue
	qsub_cmd = "qsub {}".format(file_name)
	call(qsub_cmd.split(" "))	

def wait_to_job():

	while True:
		if os.path.isfile("flag_job_is_done"):
			break
		time.sleep(10)
	
def wait_to_file(path):
	
	while True:
		if os.path.isfile(path) and os.stat(path).st_size > 0:
			break
		time.sleep(2)
		
def build_tree(dir_name, concat_dir, name):

	os.makedirs(dir_name)
	os.chdir(dir_name)
	
	align_phylip = os.path.join(concat_dir, "concat.phylip") 
	partitions = os.path.join(concat_dir, "concat_partitions") 

	cmd = EXAML_CMD.format(align_phylip = align_phylip, 
						partitions = partitions, name = name)
	run_qsub("qsub_run_examl.sh", cmd)
	
	os.chdir("../")

def create_list(root, suffix, output_name):
	
	paths = {}
	#for each alignment of a gene
	for file in os.listdir(root):
		if file.endswith(suffix):
			full_path = os.path.join(root,file)
			paths[file] = full_path
						
	with open(output_name, "w") as fout:
		for file in sorted(paths, key=paths.get):
			fout.write(paths[file] + "\n")

			
def concat(dir_name, sequences_dir, suffix):	
	
	os.makedirs(dir_name)
	os.chdir(dir_name)
	
	#create paths file 
	paths_file = "sequences_paths.ls"
	create_list(sequences_dir, suffix, paths_file)
	wait_to_file(paths_file)
	
	#concatenate 
	#cmd = 'python ~/code/concat_alignments.py {}'.format(paths_file)
	#call(cmd.split(" "))
	ca.concat_alignments(paths_file)
	
	os.chdir("../")
	
def align_with_mafft():
	
	os.makedirs("aligned_by_mafft")
	os.chdir("aligned_by_mafft")

	root = "../sequences"
	cmd = MAFFT_MODULE
	for file in os.listdir(root):
		if file.endswith(".fasta"):
		
			gene_name = file.split('_')[0]
			
			cmd += MAFFT_CMD.format(input = os.path.join(root,file),
									gene = gene_name)
			cmd += "\n"
			#flag_file = "flag_mafft_{gene}_done".format(gene = gene_name)
			#cmd += "touch " + flag_file
			
	run_qsub("qsub_mafft.sh".format(gene = gene_name), cmd)
			
	wait_to_job()		
			
	os.chdir("../")
	
def aligned_by_indelible(species_list,i):	

	os.makedirs("aligned_by_indelible")
	os.chdir("aligned_by_indelible")
	filter_sequences(i, species_list, INDELIBLE_SEQS_ALIGNED)	
	os.chdir("../")
	
def get_foramt(path):
	with open(path, 'r') as f:
		line = f.readline()
	if ">" in line: 
		return "fasta"
	return "phylip"
	
def filter_sequences(i, species_list, sequences):

	#get input species
	with open(species_list, 'r') as fin:
		input_species = fin.read().splitlines()
	
	filter_dic = {}
	for gene in GENES:
		sequences_file = sequences.format(gene = gene, i = i)
		output_name = "{gene}_filtered.fasta".format(gene = gene)
		
		#read sequences - get sequences records
		format = get_foramt(sequences_file)
		sequences_records = list(SeqIO.parse(sequences_file, format))
	
		filtered = [record for record in sequences_records 
					if record.id in input_species]
		
		filter_dic[sequences_file] = [len(sequences_records), len(filtered)]
		
		if len(filtered) <= 1:
			continue
		
		with open(output_name, 'w') as outf:
			for record in filtered:
				id = ">" + record.id + "\n"
				sequence = str(record.seq).replace('\n', '') + '\n'
				outf.write(id)
				outf.write(sequence)
	
	with open("filtering.logfile", 'w') as f:
		f.write("species list:\n" + species_list + "\n")
		for key, value in filter_dic.iteritems(): 
			f.write("file: " + key + "\n")
			f.write("# seqs before and after filtering:	" + str(value) + "\n")
	
def get_sequences(i, species_list):
	os.makedirs("sequences")
	os.chdir("sequences")
	filter_sequences(i, species_list, INDELIBLE_SEQS_UNALIGNED)	
	os.chdir("../")

def trimAL(dir_name, dir_files, trimal_gapthreshold):
	
	os.makedirs(dir_name)
	os.chdir(dir_name)
	
	for file in os.listdir(dir_files):
		if file.endswith((".fasta", ".mafft")):
			align = os.path.join(dir_files,file)
			run_trimal.trimal(align, file, trimal_gapthreshold)	
	
	os.chdir("../")
	
def main(species_list, output_name, num_simulations, trimal_gapthreshold):
	
	for i in range(1,num_simulations+1):
	
		dir_name = "{}_{}".format(output_name,i)
		
		os.makedirs(dir_name)
		os.chdir(dir_name)
		
		logging.info("starting directory {}".format(i))
		
		logging.info("getting sequences")
		
		#filter simulated sequences
		get_sequences(i, species_list)
		
		logging.info("starting aligning")
		
		align_with_mafft()
		aligned_by_indelible(species_list,i)
		
		if trimal_gapthreshold > -1:
		
			logging.info("starting trimal")
		
			trimAL("trimal_mafft", "../aligned_by_mafft", trimal_gapthreshold)
			trimAL("trimal_indelible", "../aligned_by_indelible", trimal_gapthreshold)
		
		logging.info("starting concating sequences")
		
		concat("concat_mafft", "../trimal_mafft", ".mafft")
		concat("concat_indelible", "../trimal_indelible", ".fasta")
		
		logging.info("starting building trees")
		
		build_tree("tree_mafft", os.path.join(os.getcwd(),"concat_mafft"), 
					dir_name)
		build_tree("tree_indelible", os.path.join(os.getcwd(),"concat_indelible"), 
					dir_name)
		
		os.chdir("../")
	
		time.sleep(1)
		
	
if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description='')
	
	parser.add_argument('--species_list', '-s', required=True,
						help='list of species')
	
	parser.add_argument('--output_name', '-o', required=True,
						help='output of folders')
	
	parser.add_argument('--trimal_gapthreshold', '-trimal', required=False,
						default=-1, help='gapthreshold of trimal')
						
	parser.add_argument('--num_simulations', '-n', required=True,
						 help='number of simulations')

	args = parser.parse_args()
	species_list = args.species_list
	output_name = args.output_name
	num_simulations = int(args.num_simulations)
	trimal_gapthreshold = float(args.trimal_gapthreshold)
	
	mylogger.initialize(output_name)
	
	logging.info("species list: {}".format(species_list))
	logging.info("output name: {}".format(output_name))
	logging.info("number of simulations: {}".format(num_simulations))
	logging.info("indelible sequences - alinged: {}".format(INDELIBLE_SEQS_ALIGNED))
	logging.info("indelible sequences - not alinged: {}".format(INDELIBLE_SEQS_UNALIGNED))
	logging.info("genes: {}".format(", ".join(GENES)))
	logging.info("gapthreshold of trimal: {}".format(trimal_gapthreshold))
		
	main(species_list, output_name, num_simulations, trimal_gapthreshold)