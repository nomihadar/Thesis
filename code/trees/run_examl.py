import os, sys
import argparse
from subprocess import call
import time
import re, math

sys.path.append("/groups/itay_mayrose/nomihadar/code/")

import run_job as rj

#NUM_THREADS = 1

MODEL = 'PROTGAMMAAUTO'
MODEL = 'GAMMA'

PARSIMONY_TREE = 'RAxML_parsimonyTree.raxml'
RAXML_INFO_FILE = 'RAxML_info.raxml'

QSUB_ARGS_EXAML = '''#!/bin/tcsh
#$ -N examl
#$ -S /bin/tcsh
#$ -cwd
#$ -l itaym
#$ -p 0
#$ -e $JOB_NAME.$JOB_ID.ER
#$ -o $JOB_NAME.$JOB_ID.OU
#$ -pe orte {num_threads}
#$ -l h=!(compute-7-1|compute-7-0)

module load rocks-openmpi
module load examl
mpiexec -np {num_threads} examl -s {alig_partition_binary} -t {raxml_tree} -m {model} -n {output_name}.tree -S
touch flag_examl_is_done
'''

LOAD = 'module load examl\nmodule load raXML\n'
CMD_RAXML = LOAD + 'raxmlHPC -y -m PROTGAMMAAUTO -p 12345 -s {alignment_phylip} -n raxml'
CMD_RAXML = LOAD + 'raxmlHPC -y -m GTRCAT -p 12345 -s {alignment_phylip} -n raxml'

def run_examl(num_threads, alignment_binary, parsimony_tree, output_name):

	#create the arguments file for qsub 
	args_file = "qsub_examl.sh"
	with open(args_file, 'w') as fout:
		qsub_args = QSUB_ARGS_EXAML.format\
						(num_threads = num_threads,
						alig_partition_binary = alignment_binary,
						raxml_tree = parsimony_tree,
						model = MODEL,
						output_name = output_name)
						
		fout.write(qsub_args)
	
	#run phlawd on queue
	qsub_cmd = "qsub {}".format(args_file)
	call(qsub_cmd.split(" "))

def run_raxml(alignment):
	#compute statistics
	cmd = CMD_RAXML.format(alignment_phylip = alignment)
	rj.run_job(cmd, "job_raxml.sh")
	
def get_num_threads():

	#open the raxml info file to get num alignment patterns
	#because the recomended num threads depends on num patterns
	#rule of thumb: thread per 500 pattrens
	if not os.path.isfile(RAXML_INFO_FILE):
		print "info file was not found"
		exit(0)
		
	with open(RAXML_INFO_FILE, 'r') as f:
		info_file = f.read()
		regex = "Alignment has (\d+) distinct alignment patterns"
		result = re.search(regex, info_file)
		num_pattrens = int(result.group(1))
		
	num_threads = max(int(num_pattrens / 500), 1)
		
	return num_threads

def wait_for_job(path):
	
	while True:
		time.sleep(5)
		
		#stop raxml running 
		if os.path.isfile(path):
			break
		
def build_parsimony_tree(alignment):

	#create a folder for the raxml output
	parsimony_dir = "parsimony"
	os.makedirs(parsimony_dir)
	os.chdir(parsimony_dir)	
	
	#run raxml
	run_raxml(alignment)
	
	#wait for the parsimony tree
	wait_for_job(PARSIMONY_TREE)
		
	#get number of threads (rule of thumb)
	num_threads = get_num_threads()
	#num_threads = 1########
	
	#get path of parsimony tree
	os.chdir("../")
	
	parsimony_tree = os.path.join(parsimony_dir, PARSIMONY_TREE)
	
	return (parsimony_tree, num_threads)
	
def convert_to_binary(msa, partitions):
	
	#create a folder for the binary output
	binary_dir = "binary"
	os.makedirs(binary_dir)
	os.chdir(binary_dir)	
	print ("nomi********************************")
	if os.path.isfile(partitions):
		cmd = 'parse-examl -s {msa} -q {partitions} -m DNA -n {name}'
		cmd = cmd.format(msa = msa, partitions = partitions, name = "concat")
	else:
		cmd = 'parse-examl -s {msa} -m DNA -n {name}'
		cmd = cmd.format(msa = msa, name = "concat")
	print (cmd)	
	call(cmd.split(" "))
	
	os.chdir("../")
	
	alignment_binary = os.path.join(binary_dir, "concat.binary")
	
	return alignment_binary
	
def main(alignment, partitions, output_name):
	
	#build a parsimony tree
	parsimony_tree, num_threads = build_parsimony_tree(alignment)
	
	#convert to binary
	alignment_binary = convert_to_binary(alignment, partitions)
	
	#run examl 
	run_examl(num_threads, alignment_binary, parsimony_tree, output_name)

	
if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--msa', '-m', required=True,
						help='msa file')
	parser.add_argument('--partitions', '-p', required=False,
						help='partitions file', default=" ")
	parser.add_argument('--output', '-o', required=True,
						help='output name')						
	args = parser.parse_args()

	main(args.msa, args.partitions, args.output)
	
'''
def kill_raxml_job():
	
	for file in os.listdir("."):
		if file.endswith(".OU"):
			job_id = re.search(".*\.(\d+)\.OU", file).group(1)

	os.system("qdel " + job_id)	
'''	