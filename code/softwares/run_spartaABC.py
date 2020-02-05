import sys
import os
import time
import argparse
from subprocess import call

sys.path.append("/groups/itay_mayrose/nomihadar/code/")

import run_job as rj
from alignments import get_min_max_boundaries_from_msa as boundaries
from trees import rescale_branches as rb

SPARTA_CMD = '/groups/pupko/elilevy/pupkoSVN/trunk/programs/SpartaABC/SpartaABC.doubleRep {config_path}'

MIN_IR_VAL = 0

CONFIG_FILE = """_indelibleTemplateControlFile {template_name}
_inputRealMSAFile {msa_path}
_outputGoodParamsFile {output_path}
_numberOfSamplesToKeep {num_iterations}
_minRLVal {minRLVal}
_maxRLVal {maxRLVal}
_minIRVal {minIRVal}
_maxIRVal {maxIRVal}
_wAvgUniqueGapSize 0.0611508168659
_wMSAMin 0.00428943267438
_wNumGapsLenTwo 0.00183773167418
_wAvgGapSize 0.158506435717
_wTotNumGaps 0.000302688690478
_wNumGapsLenAtLeastFour 0.000586312813355
_wNumGapsLenOne 0.000943599261764
_wMSAMax 0.00332419698552
_wMSALen 0.0005140817814
_wTotNumUniqueGaps 0.00248790123796
_wNumGapsLenThree 0.00300439144851

"""

TEMPLATE_CTRL_FILE = """[TYPE] NUCLEOTIDE 2	
	
[SETTINGS]
	[output] FASTA
  [fileperrep] TRUE 
[MODEL]    modelname        
  [submodel]  HKY 2.5                	
  [statefreq] 0.25 0.25 0.25 0.25
  [indelmodel]  POW  1.3 50 
  [indelrate]   0.02

//balibase 233
[TREE] treename 
{tree}

[PARTITIONS]   partitionname           
  [treename modelname  350]

[EVOLVE] partitionname 1 try

"""

def runSparta(gene, config_path, maxIRVal):

	#run spartaABC
	cmd = SPARTA_CMD.format(config_path = config_path)
	rj.run_job(cmd, "job_spartaABC.sh")	
	
def create_config_file(gene, config_path, template_name, 
						num_iterations, maxIRVal, msa_path, output_path):
	
	msa_path = msa_path.format(gene = gene)
	output_path = output_path.format(gene = gene)

	#get min and max values of the root length (RL) parameter
	(minRLVal, maxRLVal) = boundaries.get_min_max_boundaries_from_msa(msa_path)

	config_file = CONFIG_FILE.format(template_name = template_name,
									msa_path = msa_path,
									output_path = output_path,
									num_iterations = num_iterations,
									minRLVal = minRLVal, 
									maxRLVal = maxRLVal,
									minIRVal = MIN_IR_VAL,
									maxIRVal = maxIRVal)
	
	return config_file

def create_template_ctrl_file(gene, template_name, tree_path):
	
	#get the tree for the template control file
	tree_path = tree_path.format(gene = gene)
	with open(tree_path, 'r') as f:
		tree = f.read().splitlines()[0]
		
	fixed_tree = rb.rescale_branches(tree)
	 
	#write the template file 
	template_file = TEMPLATE_CTRL_FILE.format(tree = fixed_tree)
	
	return template_file
	
def write_file(file_name, file_content):
	with open (file_name, "w") as fout:
		fout.write(file_content)

	
def main(gene, maxIRVal, num_iterations, 
		num_jobs, tree_path, msa_path, output_path):
	
	config_path = "spartaABC_config_{gene}".format(gene=gene)
	template_name = "template_control_{gene}.txt".format(gene=gene)
	
	config_content = create_config_file(gene, config_path, template_name, 
										num_iterations, maxIRVal, 
										msa_path, output_path)
										
	template_content = create_template_ctrl_file(gene, template_name, tree_path)
	
	#run in pipeline
	for i in range(num_jobs):
		
		dir_name = gene + str(i)
		os.makedirs(dir_name)
		os.chdir(dir_name)
		
		write_file(config_path, config_content)
		write_file(template_name, template_content)
		
		runSparta(gene, config_path, maxIRVal)
		
		os.chdir("../")
			
		time.sleep(5)
		
def main_paths(gene, maxIRVal, num_iterations, 
		num_jobs, tree_path, paths_file, output_path):
	
	with open(paths_file, 'r') as f:
		msa_files = f.read().splitlines()
		
	for msa_file in msa_files:
		dir = os.path.basename(msa_file)
		os.makedirs(dir)
		os.chdir(dir)
		
		main(gene, maxIRVal, num_iterations, 
			num_jobs, tree_path, msa_file, output_path)
		
		os.chdir("../")
		
		
if __name__ == "__main__":

	
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('-gene', required=True,
						help='name of gene')
	parser.add_argument('-max_ir', required=True, type=float,
						help='maximal value of ir')
	parser.add_argument('--num_iterations', '-n', required=True,
						type=int, help='number of iterations')
	parser.add_argument('--num_jobs', '-nn', required=True,
						type=int, help='number of jobs')
	parser.add_argument('--tree', '-t', required=True,
						help='tree')
	parser.add_argument('--msa', '-m', required=True,
						help='path of alignment')
	parser.add_argument('--output_path', '-o', required=True,
						help='output path')
	parser.add_argument('-paths', action='store_true', 
						help='file contains paths')
	args = parser.parse_args()
	
	if args.paths:
		main_paths(args.gene, args.max_ir, args.num_iterations, 
				args.num_jobs, args.tree, args.msa, args.output_path)
	else:
		main(args.gene, args.max_ir, args.num_iterations, 
			args.num_jobs, args.tree, args.msa, args.output_path)







