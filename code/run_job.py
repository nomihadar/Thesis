import os
import sys
import argparse
from subprocess import call

sys.path.append("/groups/itay_mayrose/nomihadar/code/")

#qsub command and arguments 
QSUB_ARGS = """#!/bin/tcsh
#$ -N job 
#$ -S /bin/tcsh
#$ -cwd
#$ -l itaym
#$ -p {priority}
#$ -e {ername}
#$ -o $JOB_NAME.$JOB_ID.OU
#$ -l h=(compute-7-0)

set history=0
module load python/python-2.7.6
{cmd}

"""
#$ -l h=!(compute-7-1|compute-7-0)
#$ -l h=(compute-7-0)
#$ -l h=(compute-8-10|compute-8-11|compute-8-12|compute-8-13|compute-8-14)

#module load python/anaconda3-4.0.0
#module load python/python-2.7.6
DIRECTORY = "run_{}"
SH_FILE = "job.sh"

CMD = 'python ~/code/statistics/user_distribution.py -f "/groups/itay_mayrose/nomihadar/working/data.indels.lengths/lengths.sic.noedges/paths.txt" -o observations_num_occurrences.csv -concat'

def run_job(cmd, sh_file = SH_FILE, priority = -1,ername="$JOB_NAME.$JOB_ID.ER"):

	#create the arguments file for qsub 
	with open(sh_file, 'w') as fout:
		qsub_args = QSUB_ARGS.format(cmd = cmd, priority = priority, ername=ername)
		fout.write(qsub_args)

	#run phlawd on queue
	qsub_cmd = "qsub {sh_file}".format(sh_file=sh_file)
	call(qsub_cmd.split(" "))

def main(command, sh_file, multiply_jobs, priority):
	
	if multiply_jobs:
		for i in range(1,num_runs+1):
			dir = DIRECTORY.format(i)
			os.makedirs(dir)
			os.chdir(dir)
			
			run_job(command, sh_file, priority)
			
			os.chdir("../")
	else:
		run_job(command, sh_file, priority)
		
if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--command', '-cmd', required=False,
						default=CMD, help='command to run')
	parser.add_argument('--multiply_jobs', '-n', action='store_true', 
						help='number of times to run command')
	parser.add_argument('--sh_file', '-sh', default= SH_FILE,
						required=False, help='name of .sh file')
	parser.add_argument('--priority', '-p', default= 0, type=int,
						required=False, help='priority of job')
	args = parser.parse_args()

	main(args.command, args.sh_file, args.multiply_jobs, args.priority)
	
	