import os
import sys
import time

from subprocess import call
from random import shuffle
from ete3 import Tree
from run_treedist import treedist 
from Bio import SeqIO 

import concat_alignments 
from run_qsub import run_qsub
import logging
import mylogger


TRUE_TREE = "/groups/itay_mayrose/nomihadar/simulations/subtrees_of_true_tree/subtrees_a/subtree_1.tree"

SMALL_TEEE_SPECIES = "/groups/itay_mayrose/nomihadar/simulations/subtrees_of_true_tree/subtrees_a/subtree_1.ls"
BIG_TEEE_SPECIES = "/groups/itay_mayrose/nomihadar/simulations/subtrees_of_true_tree/subtrees_a/subtree_2.ls"

INDELIBLE_SEQS_PHYLIP_PATH = "/groups/itay_mayrose/nomihadar/simulations/simulated_sequences/4_genes_cover/indelible_random_param/{gene}/{gene}_TRUE_{i}.phy" 

JOB_FLAG = "flag_job_is_done"
EXAML_FLAG = "flag_examl_is_done"

GENES = ['18S', '26S', 'atpB', 'rbcL', 'matK', 'ITS', 'trnLtrnF']

QSUB_ARGS = """#!/bin/tcsh
#$ -N python 
#$ -S /bin/tcsh
#$ -cwd
#$ -l itaym
#$ -p -0
#$ -e $JOB_NAME.$JOB_ID.ER
#$ -o $JOB_NAME.$JOB_ID.OU

module load python/python-2.7.6
{cmd}
touch flag_job_is_done
"""

def get_foramt(path):
	with open(path, 'r') as f:
		line = f.readline()
	if ">" in line: 
		return "fasta"
	return "phylip"

def wait_to_job(flag):
	#check if all are done
	while True:
		if os.path.isfile(flag):
			break
		time.sleep(10)
	
def wait_to_file(path):
	
	#check if all are done
	while True:
		if os.path.isfile(path) and os.stat(path).st_size > 0:
			break
		time.sleep(2)
		

def read_species(path):
	with open (path, 'r') as f:
		species_ls = f.read().splitlines() 
	return species_ls

def filter_sequences(i, species_list, sequences):
	
	filter_dic = {}
	for gene in GENES:
		sequences_file = sequences.format(gene = gene, i = i)
		output_name = "{gene}_filtered.fasta".format(gene = gene)
		
		#read sequences - get sequences records
		format = get_foramt(sequences_file)
		sequences_records = list(SeqIO.parse(sequences_file, format))
	
		filtered = [record for record in sequences_records 
					if record.id in species_list]
		
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
		f.write("species list:\n" + '\n'.join(species_list) + "\n")
		for key, value in filter_dic.iteritems(): 
			f.write("file: " + key + "\n")
			f.write("# seqs before and after filtering:	" + str(value) + "\n")	
	
def aligned_by_indelible(species_list,i=1):	

	os.makedirs("aligned_by_indelible")
	os.chdir("aligned_by_indelible")
	filter_sequences(i, species_list, INDELIBLE_SEQS_PHYLIP_PATH)	
	os.chdir("../")	
	
def concat(dir_name, sequences_dir, suffix):	
	
	os.makedirs(dir_name)
	os.chdir(dir_name)
	
	#create paths file 
	paths_file = "sequences_paths.ls"
	create_list(sequences_dir, suffix, paths_file)
	wait_to_file(paths_file)
	
	#concatenate 
	concat_alignments.concat_alignments(paths_file)
	
	concat_alignment = os.path.abspath("concat.phylip")
	concat_partitions = os.path.abspath("concat_partitions")
	
	os.chdir("../")
	
	return concat_alignment, concat_partitions
	
	
def build_tree(dir_name, alignment, paritions, name):
	
	os.makedirs(dir_name)
	os.chdir(dir_name)
	
	cmd = 'python ~/code/run_examl.py {alignment} {paritions} {name}'\
			.format(alignment = alignment, 
					paritions = paritions, 
					name = name)
	run_qsub(cmd, "qsub_run_examl.sh")
	
	tree_path = os.path.join(os.getcwd(), "ExaML_result.{}.tree".format(name))			
	flag = os.path.join(os.getcwd(), EXAML_FLAG)
	
	os.chdir("../")	
	
	return tree_path, flag
	
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
	
def build_tree_pipeline(species_list, output_name):
	
	if os.path.exists(output_name):
		os.system("rm -rf " + output_name)
	
	os.makedirs(output_name)
	os.chdir(output_name)
	
	aligned_by_indelible(species_list)
	concat_alignment, concat_partitions = concat("concat_indelible", 
										"../aligned_by_indelible", ".fasta")
	tree_path, flag = build_tree("tree_indelible", concat_alignment, 
								concat_partitions, output_name)
	
	os.chdir("../")
	
	return tree_path, flag
	
def split_list(a_list):
    half = int(len(a_list)/2)
    return a_list[:half], a_list[half:]	

def prune_tree(tree_path, species_ls, output_name):

	tree = Tree(tree_path)
	tree.prune(species_ls, preserve_branch_length=True)
	tree.write(outfile = output_name, format = 1)
	
def lion_in_desert2(small_tree_species, species):
	
	DIST = 0.409
	
	logging.info("distance to compare: " + str(DIST))
	logging.info("iteration,# species,distance,difference,species")
	
	i = 0 
	while True:
	
		os.makedirs('iteration_' + str(i))
		os.chdir('iteration_' + str(i))
		
		shuffle(species)
		
		split1 = species[:-10]
		split2 = species[10:]
		
		tree1, flag1 = build_tree_pipeline(split1 + small_tree_species, str(1))
		tree2, flag2 = build_tree_pipeline(split2 + small_tree_species, str(2))
		
		wait_to_job(flag1)
		wait_to_job(flag2)
		
		prune_tree(tree1, small_tree_species, "tree1_pruned.tree")
		prune_tree(tree2, small_tree_species, "tree2_pruned.tree")
		
		dist1 = treedist(TRUE_TREE, "tree1_pruned.tree")["bs"] #branch score
		dist2 = treedist(TRUE_TREE, "tree2_pruned.tree")["bs"]
		
		diff1 = abs(dist1 - DIST)
		diff2 = abs(dist2 - DIST)
		
		if diff1 <= diff2:
			species = split1
			logging.info("{},{},{},{},{}".format(i,len(split1),dist1,
												diff1,','.join(species)))
		else:
			species = split2
			logging.info("{},{},{},{},{}".format(i,len(split2),dist2,
												diff2,','.join(species)))
		
		if not split1 or not split2:
			break
		
		os.chdir("../")
		i += 1
	
	
def lion_in_desert(small_tree_species, species):
	
	
	DIST = 1.20656803333333
	DIST = 0.409
	
	logging.info("distance to compare: " + str(DIST))
	logging.info("iteration,# species,distance,difference,species")
	
	i = 0 
	while True:
	
		os.makedirs('iteration_' + str(i))
		os.chdir('iteration_' + str(i))
		
		shuffle(species)
		
		split1, split2 = split_list(species)
		
		tree1, flag1 = build_tree_pipeline(split1 + small_tree_species, str(1))
		tree2, flag2 = build_tree_pipeline(split2 + small_tree_species, str(2))
		
		wait_to_job(flag1)
		wait_to_job(flag2)
		
		prune_tree(tree1, small_tree_species, "tree1_pruned.tree")
		prune_tree(tree2, small_tree_species, "tree2_pruned.tree")
		
		dist1 = treedist(TRUE_TREE, "tree1_pruned.tree")[1] #branch score
		dist2 = treedist(TRUE_TREE, "tree2_pruned.tree")[1]
		
		diff1 = abs(dist1 - DIST)
		diff2 = abs(dist2 - DIST)
		
		if diff1 <= diff2:
			species = split1
			logging.info("{},{},{},{},{}".format(i,len(split1),dist1,
												diff1,','.join(species)))
		else:
			species = split2
			logging.info("{},{},{},{},{}".format(i,len(split2),dist2,
												diff2,','.join(species)))
		
		if not split1 or not split2:
			break
		
		os.chdir("../")
		i += 1

def main():

	logging.info("true tree: " + TRUE_TREE)
	logging.info("small tree speicies: " + SMALL_TEEE_SPECIES)
	logging.info("big tree speicies: " + BIG_TEEE_SPECIES)

	small_species = read_species(SMALL_TEEE_SPECIES)
	big_species = read_species(BIG_TEEE_SPECIES)
	
	logging.info("# species in small tree: " + str(len(small_species)))
	logging.info("# species in big tree: " + str(len(big_species)))
	
	species_in_big_only = [species for species in big_species 
							if species not in small_species]
	
	lion_in_desert2(small_species, species_in_big_only)
	
if __name__ == "__main__":

	if len(sys.argv) < 1:
		print "please insert argument"
		sys.exit(0)
	
	mylogger.initialize(__file__)

	main()