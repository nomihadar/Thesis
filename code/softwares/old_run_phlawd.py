"""
Goal: 		run phlawd on several loci
Input args: 1. a table with list of genes and their parameters for the 
				configuration file.
			2. sequences of role plants for reference sequences
			3. partitions for the above sequences
Author:		Nomi Hadar
Date:		Januar 2016
"""

# argv[0] = "plos_one/my_table_s1.csv"
# argv[1] = "plos_one/get_refernce_seqs/seqs_of_Fabacea_from_plosone_alignment"
# argv[2] = "plos_one/Streptophytina_by_genus_partitions.part.reduced"
import sys
import os
import datetime
import numpy as np
from subprocess import call
import fnmatch
from Bio import AlignIO
'Magnoliophyta'
'rosids'
'fabids'
'Fabales'
'Fabaceae'
CLADE = 'Magnoliophyta'
OUTPUT_DIR = "phlawd_{clade}_mad_0.5".format(clade = CLADE)

#qsub command and arguments 
QSUB_CMD = "qsub %s"
QSUB_ARGS = """#!/bin/tcsh
#$ -N job_%s
#$ -S /bin/tcsh
#$ -cwd
#$ -l itaym
#$ -p 0
#$ -e %s/$JOB_NAME.qsub.ER
#$ -o %s/$JOB_NAME.qsub.OU
%s
"""

PHLAWD_CONFIG_FILE = """clade = %s
db = /groups/itay_mayrose/nivsabath/big.tree/pln.db 
mad = 0.5
coverage = %.2f
identity = %.2f
gene = %s
knownfile = %s 
numthreads = 8

search = %s
searchliteral
"""
#searchliteral if with search
###############################################################################
# 
###############################################################################

def run_phlawd(config_file_path, sub_dir, gene):
	
	# create PHLAWD command 
	PHLAWD_command = "PHLAWD assemble %s" % config_file_path
	
	#create the arguments file for qsub 
	qsub_file_path = "%s/qsub_arguments.sh" % sub_dir
	qsub_arguments = QSUB_ARGS % (gene, sub_dir, sub_dir, PHLAWD_command)
	fo = open(qsub_file_path, "w")
	fo.write(qsub_arguments)
	fo.close()
	
	#run phlawd on queue
	qsub_command = QSUB_CMD % qsub_file_path
	call(qsub_command.split(" "))

def convert_to_sql_query(and_or_query):

	#example = description LIKE '%ITS%'
	description = 'description LIKE \'%{0}%\''
	query = ""

	#split by OR ("|")
	or_splited = and_or_query.split("|")
	
	for i, o in enumerate(or_splited):
		
		if not "&" in o:
			query += description.format(o.strip())
			if i < len(or_splited)-1:
				query += " OR "
			
		else:
			and_splited = o.split("&")
			
			query += "("
			for j, a in enumerate(and_splited):
				query += description.format(a.strip())
				if j < len(and_splited)-1:
					query += " AND "
			query += ")"
				
			if i < len(or_splited)-1:
				query += " OR "
	
	if query[0] is not "(":
		query = "(" + query + ")"
			
	return query

def get_search_field(include_search, exclude_search):
	#convert the include_search to a sql format
	sql_query = convert_to_sql_query(include_search)
	#convert the exclude_search to a sql format
	if exclude_search:
		sql_query += " AND NOT " + convert_to_sql_query(exclude_search)
	
	return sql_query
		
def create_config_file(parameters, output_path, knownfile_path):
	
	#extract gene's parameters
	gene = parameters['gene']
	coverage = parameters['coverage']
	identity = parameters['identity']
	include_search = parameters['include_search']
	exclude_search = parameters['exclude_search']
	
	#with search
	search_field = get_search_field(include_search, exclude_search)
	
	#without search
	#search_field = gene
	
	#create the configuration's content
	config_content = PHLAWD_CONFIG_FILE % (CLADE, coverage, identity, 
										os.path.join(output_path,gene), 
										knownfile_path, search_field)
										
	#create the configuration file
	config_path = os.path.join(output_path, "%s_config.PHLAWD" % gene)
	fo = open(config_path, "w")
	fo.write(config_content)
	fo.close()
	
	return config_path
	
 
#create the known file which is the file with the reference sequence
def create_knownfile(partitions, seqs_dic, sub_dir, gene):
	
	#get positions of current gene in the alignment
	(start,end) = partitions[gene.lower()]
	
	ref_seq_found = False
	#find a non empty sequence of the gene  
	for plant_model, seq in seqs_dic.iteritems():
	
		gene_seq = seq[start:end]
		
		# if "max" in plant_model:
			# print plant_model
		#if the gene is not empty 
		if gene_seq.count('-') != len(gene_seq) and plant_model == "Glycine_max":
		
			ref_seq_found = True
		
			#get the position of current gene
			knownfile_content = gene_seq.replace("-","")
			
			break
	
	if not ref_seq_found:
		return "ref seq not found"
		
	#create the .keep file (knownfile)
	knownfile_name = "%s_%s.keep" % (plant_model, gene)
	knownfile_path = os.path.join(sub_dir, knownfile_name)
	
	fo = open(knownfile_path, "w")
	fo.write(">%s\n" % gene)
	fo.write(knownfile_content)
	fo.close()
	
	#return the path to the .keep file
	return knownfile_path

#read seqs 
def read_phylip_seqs(align_path):
	
	#read sequences (in pylip format)
	seqs_dic = {}

	with open(align_path) as f:
		for i, line in enumerate(f):
			if i == 0:
				continue
			
			splited = line.split()
			if splited:
				species = splited[0]
				
				conc_seqs = splited[1]
				seqs_dic[species] = conc_seqs
	
	return seqs_dic	
	
###############################################################################
if len(sys.argv) < 4:
	print "please insert arguments"
	sys.exit(0)

#get the path of the root directory 
genes_list_path = sys.argv[1]
reference_seqs_path = sys.argv[2]
partitions_path = sys.argv[3]

#create a directory to the output of this script 
if not os.path.exists(OUTPUT_DIR):
	current_date = datetime.datetime.now().strftime('%d-%m-%Y')
	output_dir_path = OUTPUT_DIR 
	os.makedirs(output_dir_path)
	
#load files ###############################################################

#load the list of genes and their parameters
header = ('gene', 'include_search', 'exclude_search', 
			'coverage', 'identity')	

genes_param = np.genfromtxt(genes_list_path, delimiter = ',',
							dtype = None, skip_header = True, 
							names = header)

#load the sequence file
# reference_seqs = np.loadtxt(reference_seqs_path, 
							# delimiter = " ", dtype = 'str')
# ref_genera = reference_seqs[:,0]
# ref_seqs = reference_seqs[:,1]
#align = AlignIO.read(reference_seqs_path, "phylip")	

seqs_dic = read_phylip_seqs(reference_seqs_path)

#load the partition file 
#get dictoinary of gene and tuple of positions(start, end)
partitions = np.loadtxt(partitions_path, delimiter = " ", dtype = 'str')
partitions_dic = {}
for _, gene, _, positions in partitions:
	(start, end) = positions.split("-")
	partitions_dic[gene.lower()] = (int(start)-1, int(end))

###########################################################################
# main code
###########################################################################

#for each gene in the genes list
for gene_param in genes_param:
	
	#get current gene
	gene = gene_param['gene']
	
	#create a sub directory for current gene
	sub_dir = os.path.join(OUTPUT_DIR, gene)
	if not os.path.exists(sub_dir):
		os.makedirs(sub_dir)
	
	#create file with reference sequence
	knownfile_path = create_knownfile(partitions_dic, seqs_dic, sub_dir, gene)
	
	if knownfile_path == "ref seq not found":
		continue
	
	#create configuration file
	config_path = create_config_file(gene_param, sub_dir, knownfile_path)
	
	#run phlawd
	run_phlawd(config_path, sub_dir, gene)

print "DONE!"