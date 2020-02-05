import sys
import os
from subprocess import call

QSUB_ARGS = '''#!/bin/tcsh
#$ -N parse_msa
#$ -S /bin/tcsh
#$ -cwd
#$ -l itaym
#$ -p 0
#$ -e $JOB_NAME.qsub.ER
#$ -o $JOB_NAME.qsub.OU

parse-examl -s {alignment} -q {partitions} -m DNA -n {output_name}
'''

def run_parse(alignment, partitions, output_name):

	#create the arguments file for qsub 
	args_file = "qsub_parse.sh"
	with open(args_file, 'w') as fout:
		qsub_args = QSUB_ARGS.format(alignment = alignment,
									partitions = partitions,
									output_name = output_name)
		fout.write(qsub_args)
	
	#run phlawd on queue
	qsub_cmd = "qsub {}".format(args_file)
	call(qsub_cmd.split(" "))
	
if __name__ == "__main__":

	if len(sys.argv) < 3:
		print "please insert arguments"
		sys.exit(0)
	
	alignment_path = sys.argv[1]
	
	#file with the list of msa 
	partitions_path = sys.argv[2]
	
	run_parse(alignment_path, partitions_path, "concat")
	
	
	
	