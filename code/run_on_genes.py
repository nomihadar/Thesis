import os
import sys
import argparse
import pandas as pd
from subprocess import call
import run_job


GENES = ['GENE{:04d}'.format(i) for i in range(1,1001)] # 5712	

GENES = ['GENE{:04d}'.format(i) for i in range(1,1001)] # 5712
GENES = ['GENE{:02d}'.format(i) for i in range(1,99)] # 5712	
GENES = ['GENE{:04d}'.format(i) for i in range(1,1001) if "GENE{:04d}_goodness.csv".format(i) not in os.listdir("/groups/itay_mayrose/nomihadar/working/data.powerlaw.goodness/bootstrap_p_other_distributions/")   ] # 5712

GENES = ['18S', '26S', 'ITS', 'atpB', 'matK', 'rbcL', 'trnLtrnF']

CMD = 'python ~/code/create_paths_list.py -r "/groups/itay_mayrose/nomihadar/simulations/dataset_big/sim_sequences/1sequences/mymethod2018/{gene}/" -s .phy -o {gene}_paths_true.txt' 

CMD = 'python ~/code/alignments/compute_statistics.py -f "/groups/itay_mayrose/nomihadar/simulations/dataset_big/sim_sequences/1sequences/mymethod2018/{gene}_paths_true.txt" -paths'

CMD = 'python ~/code/softwares/run_guidance.py -b 20 -s "/groups/itay_mayrose/nomihadar/simulations/dataset_big/sim_sequences/5blocks/block_optimized_sampled/{gene}_paths_.txt" -paths -rm'


CMD = 'python ~/code/softwares/run_guidance.py -b 20 -s "/groups/itay_mayrose/nomihadar/simulations/dataset_big/sim_sequences/5blocks/block_optimized_sampled/{gene}_paths_.txt" -paths -rm'


CMD = 'python ~/code/softwares/guidance_collect_scores.py -root -f "/groups/itay_mayrose/nomihadar/simulations/dataset_small/sim_sequences/7removed_edges/guidance/outputs/{gene}/"'

# -maxlength 
SH_FILE = "job.sh"
SH_FILE2 = "job_{}.sh"

def temp_main4(command, sh_file):
	
	for edges in ['noedges']:
		for p in [0.1,0.05]:
			for max in [30,50,"none"]:
				dir='{}.{}.percent.max.{}'.format(edges,int(p*100),max)
				os.makedirs(dir)
				os.chdir(dir)
				cmd = ''
				for gene in GENES:
					sh_file = SH_FILE2.format(gene)
					max_int = max if max != "none" else 0 
					cmd += CMD.format(gene=gene,edges=edges,p=p,max=max, max_int=max_int,p_int=int(p*100))
					#cmd = CMD.format(gene=gene,edges=edges,p=p,max=max)
					cmd += "\n"
				run_job.run_job(cmd, sh_file)
				os.chdir("../")	
				
def temp_main3(command, sh_file):
	
	for edges in ['noedges']:
		for p in [0.1,0.05]:
			for max in [30,50,"none"]:
				dir='{}.{}.percent.max.{}'.format(edges,int(p*100),max)
				#os.makedirs(dir)
				#os.chdir(dir)
				max_i = max if max != "none" else 0 
				sh_file = SH_FILE2.format(dir)
				cmd = CMD.format(edges=edges,p=p,max=max, max_i=max_i,name=dir,p_int=int(p*100))
				run_job.run_job(cmd, sh_file)
				#os.chdir("../")

def main(command, sh_file):
	cmd = ''
	for gene in GENES:
		os.makedirs(gene)
		os.chdir(gene)	
		for i in range(1,31):
			os.makedirs(str(i))
			os.chdir(str(i))
			cmd = CMD.format(gene=gene,i=i) + '\n'	
			run_job.run_job(cmd, sh_file, priority=0)
			os.chdir("../")	
		cmd = ''	
		os.chdir("../")

#each gene in its own directory
def main1(command, sh_file):
	for gene in GENES:
		os.makedirs(gene)
		os.chdir(gene)
		
		cmd = CMD.format(gene=gene)
		run_job.run_job(cmd, sh_file)
		
		os.chdir("../")			

#all genes in same directory with a single .sh file		
def main2(command, sh_file):
	cmd = ''
	for gene in GENES:
		cmd += CMD.format(gene=gene) + '\n'
	run_job.run_job(cmd, sh_file, 0)

#all genes in same directory with separate .sh files	
def main3(command, sh_file):
	for gene in GENES:
		sh_file = SH_FILE2.format(gene)
		cmd = CMD.format(gene=gene)
		run_job.run_job(cmd, sh_file) #ername=gene + "_progress.txt"
		
def main4(command, sh_file, paths_file):
	with open(paths_file, 'r') as f:
		paths = f.read().splitlines()
		
	for path in paths:
		gene = os.path.basename(path)
		os.makedirs(gene)
		os.chdir(gene)
	
		cmd = CMD.format(gene=gene, path=path)
		run_job.run_job(cmd, sh_file)
		
		os.chdir("../")
	
if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--command', '-cmd', required=False,
						default=CMD, help='command to run')
	parser.add_argument('--sh_file', '-sh', default= SH_FILE,
						required=False, help='name of .sh file')
	parser.add_argument('-dirs', action='store_true',
						help="each gene in its own directory")
	parser.add_argument('-single', action='store_true',
						help="concatenate commands to a single sh file")
	parser.add_argument('-other', action='store_true',
						help="concatenate commands to a single command")
	parser.add_argument('-paths', help="paths")
	args = parser.parse_args()
	
	if args.dirs:
		main1(args.command, args.sh_file)
	elif args.single:
		main2(args.command, args.sh_file)
	elif not args.dirs and not args.single and not args.other:
		main3(args.command, args.sh_file)	
	elif args.other:
		temp_main3(args.command, args.sh_file)	
	
	
	
