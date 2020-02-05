import os, sys
import re, argparse
import numpy as np
from subprocess import call

sys.path.append("/groups/itay_mayrose/nomihadar/code/")

import run_job as rj

CMD =  'perl /groups/pupko/haim/Scripts/IndelCoder.pl {msa_file} SIC FILE /groups/pupko/haim/pupkoSVN/trunk/programs/indelCoder/indelCoder.V1.72 {edges} > &! {output}.std'


INFO_FILE = {0: ".SIC_CODED.info", 1: ".MASKED_START_END_INDELS.SIC_CODED.info"}

def count_indels(msa_file, edges, output):

	#edges is boolean
	#0=count, 1=don't count
	#if the user specify "-edges" -> edges=True=1 -> don't count
	cmd = CMD.format(msa_file = msa_file,
					edges = int(edges), 
					output = output)
	#rj.run_job(cmd, "job_count_unique.sh")
	
	call(cmd.split())
	
 
def main(msa_file, edges, output):

	#cp the input to working directory
	#because output is sent to to the wd
	cmd = "cp {} .".format(msa_file)
	call(cmd.split())
	
	msa_file_copied = os.path.basename(msa_file)
	count_indels(msa_file_copied, edges, output)
	
	#read output
	infofile = INFO_FILE[int(edges)]
	with open(infofile, 'r') as f:
		content = f.read() 
	
	lengths_str = re.findall(r'^Length: (\d+)', content, flags=re.MULTILINE)
	lengths = list(map(int,lengths_str))
	
	#save unique indels
	np.savetxt(output, lengths, '%d')
	
	#remove copied msa file
	cmd = "rm {}".format(msa_file_copied)
	call(cmd.split())
	
if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--msa_file', '-m', required=True, 
						help='alignment file')
	parser.add_argument('-no_edges', action='store_true',
						help='if specified do not include edges')
	parser.add_argument('--output', '-o', required=False,
						help='output name')					
	args = parser.parse_args()
	
	
	main(args.msa_file, args.no_edges, args.output)

		
