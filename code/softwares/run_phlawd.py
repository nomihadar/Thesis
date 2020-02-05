"""
Goal: 		run phlawd on several loci
Input args: 1. a table with list of genes and their parameters for the 
				configuration file
			2. reference sequences for each gene
			3. clade
			4. suffix name
Author:		Nomi Hadar
Date:		June 2016
"""

import sys
import os
import numpy as np
from subprocess import call
import re
from os import listdir
from os.path import isfile, join


#qsub command and arguments 
QSUB_ARGS = """#!/bin/tcsh
#$ -N phlawd_{gene_name}_{clade}
#$ -S /bin/tcsh
#$ -cwd
#$ -l itaym
#$ -p 0
#$ -e $JOB_NAME.ER 
#$ -o $JOB_NAME.OU 
{command}

"""

CONFIG_PATH = "{}_config.PHLAWD"
CONFIG_FILE = """clade = {clade}
gene = {gene_name}
mad = {mad}
coverage = {coverage}
identity = {identity}
knownfile = {gene_name}.keep 
numthreads = 8
db = /groups/itay_mayrose/nomihadar/.phlawd_db/pln.db

search = {search}
searchliteral
"""

class Gene:
   
   def __init__(self, name, mad, coverage, identity, 
				include_search, exclude_search, knownfile=''):
		self.name = name
		self.mad = mad		
		self.coverage = coverage 	
		self.identity = identity	   	 
		self.include_search = include_search	 
		self.exclude_search = exclude_search
		self.knownfile = knownfile
		
   def displayGene(self):
		print "Name: ", self.name

"""
read the table of genes parameters 
"""		
def read_parameters(parameters_path):
	
	#load the list of genes and their parameters
	header = ('gene', 'include_search', 'exclude_search', 
			 'mad', 'coverage', 'identity')	
	
	table = np.genfromtxt(parameters_path, delimiter = ',',
							dtype = None, skip_header = True, 
							names = header)
	
	#copy input file to output dir
	cp_cmd = "cp {} .".format(parameters_path)
	call(cp_cmd.split(" "))
	
	return table
	
"""
read references sequences (fasta file)
"""								
def read_ref_seq(knownfiles_dir):
	
	ref_pathes = {}
	for file in os.listdir(knownfiles_dir):
		
		gene_name = re.search("(.*).keep", file).group(1)
		path = join(knownfiles_dir, file)
		
		ref_pathes[gene_name] = path		
	# fasta_sequences = SeqIO.parse(open(references_path),'fasta')
	
	# ref_seq_dic = {}
	# for fasta in fasta_sequences:
		# ref_seq_dic[fasta.id] = str(fasta.seq)
		
	# #copy input file to output dir
	# cp_cmd = "cp {} .".format(references_path)
	# call(cp_cmd.split(" "))
	
	return ref_pathes
	
"""
create Genes objects
"""
def create_genes_objects(genes_table, ref_dic):
	
	genes = [] 
	for row in genes_table:
		
		#create an object
		gene = Gene(name = row['gene'], 
					mad = row['mad'], 
					coverage = row['coverage'], 
					identity = row['identity'], 
					include_search = row['include_search'], 
					exclude_search = row['exclude_search'],
					knownfile = ref_dic[row['gene']])
		
		genes.append(gene)
				
	return genes

def query_to_sql(and_or_query):

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

def get_search_field(gene):
	
	#convert the include_search to a sql format
	sql_query = query_to_sql(gene.include_search)
	
	#convert the exclude_search to a sql format
	if gene.exclude_search:
		sql_query += " AND NOT " + query_to_sql(gene.exclude_search)
	
	return sql_query

"""
create the configuration file
"""
def create_config_file(gene, clade):
	
	#with search
	search_field = get_search_field(gene)
	
	#create the configuration's content
	config_content = CONFIG_FILE.format\
					(clade = clade, gene_name = gene.name, 
					mad = gene.mad, coverage = gene.coverage, 
					identity = gene.identity, search = search_field)
											
	#create the configuration file
	config_path = CONFIG_PATH.format(gene.name)
	with open (config_path, 'w') as fout:
		fout.write(config_content)

"""	
create the known file which contains the reference sequence
"""
def create_knownfile(gene):
	
	#copy input file to output dir
	cp_cmd = "cp {} .".format(gene.knownfile)
	call(cp_cmd.split(" "))

def run_phlawd(gene, clade):
	
	# create PHLAWD command 
	config_path = CONFIG_PATH.format(gene.name)
	phlawd_cmd = "PHLAWD assemble {config}".format(config = config_path)
	
	#create the arguments file for qsub 
	args_file = "qsub_arguments.sh"
	with open(args_file, 'w') as fout:
		qsub_args = QSUB_ARGS.format(gene_name = gene.name, 
									command = phlawd_cmd,
									clade = clade)
		fout.write(qsub_args)
	
	#run phlawd on queue
	qsub_cmd = "qsub {}".format(args_file)
	call(qsub_cmd.split(" "))		

"""
create output dir and change dir into it
"""
def create_output_dir(clade, output_suffix):

	#create a directory to the output
	output_dir = "phlawd_{}_{}".format(clade, output_suffix)	
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)
		os.chdir(output_dir)
	else:
		print "output directory already exists"
		sys.exit(0)
			
	
"""
main function
"""	
def start(genes, clade):
	
	#for each gene in the genes list
	for gene in genes:

		#create a sub directory for current gene
		os.makedirs(gene.name)
		os.chdir(gene.name)
		
		#create file with reference sequence
		create_knownfile(gene)
		
		#create configuration file
		create_config_file(gene, clade)
		
		#run phlawd
		run_phlawd(gene, clade)
		
		os.chdir("../")
		
		
if __name__ == "__main__":

	if len(sys.argv) < 4:
		print "please insert arguments"
		sys.exit(0)
		
	#get path to table of parameters of the genes 
	parameters_path = sys.argv[1]
	
	#get path to references sequences of the genes 
	references_path = sys.argv[2]
	
	#get clade
	clade = sys.argv[3]
	
	#get the suffix of output file
	output_suffix = sys.argv[4]
	
	#create an output directory 
	create_output_dir(clade, output_suffix)
	
	#read input files 
	genes_table = read_parameters(parameters_path)
	ref_seq_dic = read_ref_seq(references_path)
	
	#create Genes objects
	genes = create_genes_objects(genes_table, ref_seq_dic)
	
	#main code
	start(genes, clade)
	
	
	print "Done!"
	
	
	
	
	
	
	