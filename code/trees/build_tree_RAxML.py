"""
Goal: 		build a tree using RAxML 
Input args: a path to a MASs file, num iteration, suffix files name
Author:		Nomi Hadar
Date:		Januar 2016
"""
import datetime
import sys
import os
from subprocess import call

time = datetime.datetime.now().strftime('_%d-%m')
OUTPUT_DIR = "output_RAxML_24_threads_CAT" + time

#an example to RAxML command:
#raxmlHPC -m GTRGAMMA -p 12345 -s dna.phy -# 20 -n T6

#-T num threads. never run it with more threads than 
#you have cores (processors/CPUs) available on your system! 
#pthread raxmlHPC-PTHREADS-SSE3 - in jekyl
NUM_THREADS = 24

#Models: GAMMA or CAT (GTRGAMMA / GTRCAT)
MODEL = "GTRCAT"

RAXML_CMD = 'raxmlHPC-PTHREADS -T {threads} -m {model} -p 12345 -s {msa_file} -n {name} -# {iterations}'

#name specific node
NODE = "comp4.itaym.q@compute-4-21.loc"

#qsub command and arguments 
QSUB_CMD = "qsub {qsub_args}"
QSUB_ARGS = """#!/bin/tcsh
#$ -N RAxML
#$ -S /bin/tcsh
#$ -cwd
#$ -l itaym
#$ -p 0
#$ -e $JOB_NAME.qsub.ER
#$ -o $JOB_NAME.qsub.OU
#$ -q {node}

{cmd}
"""

#run raxml via queue 
def run_raxml(msa_path, num_iterations, files_name):
	
	#RAxML command
	RAxML_command = RAXML_CMD.format(model = MODEL,
									threads = NUM_THREADS, 
									msa_file = msa_path,
									iterations = num_iterations,
									name = files_name) 
					
	#create the arguments file for qsub 
	qsub_args_file = "qsub_arguments.sh" 
	qsub_arguments = QSUB_ARGS.format(node = NODE, cmd = RAxML_command)
	with open(qsub_args_file, "w") as f:
		f.write(qsub_arguments)
	
	#qsub command
	qsub_command = QSUB_CMD.format(qsub_args = qsub_args_file)
	
	call(qsub_command.split(" "))
	

if __name__ == "__main__":

	if len(sys.argv) < 4:
		print "please insert arguments"
		sys.exit(0)
		
	#get the path of the root directory 
	msa_path = sys.argv[1]
	num_iterations = sys.argv[2]
	files_name = sys.argv[3]
	
	#arguments for RAxML
	raxml_args = (msa_path, num_iterations, files_name)
	
	#create a directory to the output of this script 
	if not os.path.exists(OUTPUT_DIR):
		os.makedirs(OUTPUT_DIR)
	
	#run RAxML
	os.chdir(OUTPUT_DIR)
	run_raxml(msa_path, num_iterations, files_name)
	os.chdir("../")
	
	