"""
Goal: 		build a tree using FastTree
Input args: a path to an alignment file
Author:		Nomi Hadar
Date:		Januar 2016
"""
import datetime
import sys
import os
from subprocess import call

time = datetime.datetime.now().strftime('_%d-%m')
OUTPUT_DIR = "/groups/itay_mayrose/nomihadar/output_trees/fastTree/output_phlawd-align_GTR+CAT-model"

OUTPUT_FILE = "output_fasttree"

#an example to RAxML command:
#'FastTree -gtr  alignment_file > tree_file'
#-gtr -nt (-nt for nucleotide, GTR+CAT model)
#-nt (Jukes-Cantor+CAT model)
#multithread = FastTreeMP 
FAST_TREE_CMD = 'FastTree -gtr -nt {alignment_file} > {output_file}'

#qsub command and arguments 
QSUB_CMD = "qsub {qsub_args}" 
QSUB_ARGS = """#!/bin/tcsh
#$ -N FastTree
#$ -S /bin/tcsh
#$ -cwd
#$ -l itaym
#$ -p 0
#$ -e $JOB_NAME.qsub.ER
#$ -o $JOB_NAME.qsub.OU

{cmd}
"""

#run fastTree via queue 
def run_fastTree(align_file):
	
	#fastTree command
	fasttree_cmd = FAST_TREE_CMD.format(alignment_file = align_file, 
										output_file = OUTPUT_FILE) 
					
	#create the arguments file for qsub 
	qsub_args_file = "qsub_arguments.sh" 
	qsub_arguments = QSUB_ARGS.format(cmd = fasttree_cmd)
	with open(qsub_args_file, "w") as f:
		f.write(qsub_arguments)
	
	#qsub command
	qsub_command = QSUB_CMD.format(qsub_args = qsub_args_file)
	
	call(qsub_command.split(" "))
	

if __name__ == "__main__":

	if len(sys.argv) < 2:
		print "please insert arguments"
		sys.exit(0)
	
	#get path to alignment file
	alignment_file = sys.argv[1]
		
	#create a directory to the output of this script 
	if not os.path.exists(OUTPUT_DIR):
		os.makedirs(OUTPUT_DIR)
	
	#run RAxML
	os.chdir(OUTPUT_DIR)
	run_fastTree(alignment_file)
	os.chdir("../")
	
	