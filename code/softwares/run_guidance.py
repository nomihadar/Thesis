import os, sys
import argparse
from subprocess import call
from ete3 import Tree
import shutil


sys.path.append("/groups/itay_mayrose/nomihadar/code/")

import run_job
import create_paths_list as create_paths

#outdir should be full path

MODULES = "module load python/python-3.3.0\nmodule load perl/perl516\nmodule load mafft/mafft7149\nmodule load FastTree/FastTree-2.1.8\n"

GUIDANCE_CMD = MODULES + 'perl /groups/pupko/haim/pupkoSVN/trunk/www/Guidance/guidance.pl --seqFile {seq_file} --msaProgram MAFFT --seqType nuc --outDir {outdir} --TreeAlg FastTree --Tree_Param "\-fastest"  --bootstrap {bootstrap}\n'

REMOVE_CMD = 'rm -rf AlternativeMSA/ \n'
REMOVE_CMD += 'find . ! -name "*msa.scr" ! -name "*.sh" ! -name "log" ! -name "*.sh" ! -name "ENDS_OK" ! -name "*.ER" -type f -delete'

def run_guidance(seq_file, bootstrap, rm=True):
	cmd = GUIDANCE_CMD.format(seq_file=seq_file, outdir=os.getcwd(), 
								bootstrap=bootstrap)
	if rm:
		cmd += REMOVE_CMD
	run_job.run_job(cmd, "job_run_guidance.sh")
	
def run_guidance_paths(paths_file, bootstrap, rm=True):

	#get input list_path
	with open(paths_file, 'r') as f:
		seq_files = f.read().splitlines()
	
	for seq_file in seq_files:
		
		 
		dir = os.path.basename(seq_file)
		
		if os.path.isdir(dir):
			ends =  os.path.join(dir,"ENDS_OK") 
			if os.path.exists(ends):
				continue
			else:
				shutil.rmtree(dir)
				
		os.makedirs(dir)
		os.chdir(dir)
		
		run_guidance(seq_file, bootstrap)
		
		os.chdir("../")
				
if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--seq_file', '-s', required=True,
						help='path of the tree', default='')
	parser.add_argument('--bootstrap', '-b', required=True, type=int,
						help='number of bootstrap')
	parser.add_argument('-paths', action='store_true', 
						help='file contains paths')
	parser.add_argument('--remove', '-rm', action='store_true', 
						help='remove files excpet scores file and log')
	parser.add_argument('-root', action='store_true', 
						help='root contains sequences file')
	args = parser.parse_args()
	
	if args.paths:
		run_guidance_paths(args.seq_file, args.bootstrap, args.remove)
	elif args.root:
		create_paths.main(args.seq_file, ".fas")
		run_guidance_paths("paths.txt", args.bootstrap, args.remove)
	else:
		run_guidance(args.seq_file, args.bootstrap, args.remove)