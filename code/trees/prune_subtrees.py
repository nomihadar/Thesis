import sys, os, time, re, argparse, logging

sys.path.append("/groups/itay_mayrose/nomihadar/code/")

import mylogger 
from run_job import run_job

PRUNE_CMD = 'python ~/code/trees/prune_tree.py -t {tree} -s {species} -o {output}'

ALIGN = "mafft" #"indelible" # "mafft" 

SPECIES_PATH = "/groups/itay_mayrose/nomihadar/simulations/subtrees_of_true_tree/subtrees_a_1/subtree_{j}.ls"
TREE_PATH = "/groups/itay_mayrose/nomihadar/simulations/subtrees_of_simulated_seqs/subtree_a_1/subtrees/subtrees_{i}/subtree_{i}_{k}/tree_{align}/ExaML_result.subtree_{i}_{k}.tree"

def prune_subtrees(num_subtrees, align, num_simulations):

	logging.info("pruned from {}:".format(num_subtrees))
	logging.info(TREE_PATH.format(i=num_subtrees, k="k", align=ALIGN))
	
	for j in range(1, num_subtrees+1):
					
		dir_name = "subtrees_{}".format(j)	
		os.makedirs(dir_name)
		os.chdir(dir_name)	
		
		species_path = SPECIES_PATH.format(j=j)

		logging.info(species_path)
		
		cmd = ''
		for k in range(1,num_simulations+1):
			tree_path = TREE_PATH.format(i=num_subtrees, k=k, align=ALIGN)
			
			output_name = "subtree_{}_{}_pruned.tree".format(j,k)
				
			cmd += PRUNE_CMD.format(tree=tree_path, species=species_path, 
									output=output_name)
			cmd += "\n"
			
		run_job(cmd, "job_prune_tree.sh")
	
		os.chdir("../")
	
def main(num_ranks, num_simulations):		
		
	for i in range(1,num_ranks+1):
	
		dir_name = "from_subtree_{i}".format(i=i)
		os.makedirs(dir_name)
		os.chdir(dir_name)		
		
		mylogger.initialize(dir_name)
		
		prune_subtrees(i, ALIGN, num_simulations)
	
		os.chdir("../")
	
if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='')
	
	parser.add_argument('--ranks', '-r', required=True,
						help='number of ranks in tree')
	
	parser.add_argument('--simulations', '-n', required=True,
						help='number of simulations')				

	args = parser.parse_args()
	num_ranks = int(args.ranks)
	num_simulations = int(args.simulations)
	
	mylogger.initialize("prune_subtrees.logfile")
	
	logging.info("num ranks: {}".format(num_ranks))
	logging.info("number of simulations: {}".format(num_simulations))
	logging.info("paths of trees: {}".format(TREE_PATH))
	logging.info("paths of species: {}".format(SPECIES_PATH))
	logging.info("alignments aligned by: {}".format(ALIGN))

	main(num_ranks, num_simulations)
	
	