import re
import os
import sys
import argparse
from ete3 import Tree
from subprocess import call
import unroot_tree
import pandas as pd

KTREEDIST_CMD = "perl /share/apps/Ktreedist_v1/Ktreedist.pl"
KTREEDIST_OUTPUT = "ktreedist_output" 

def extract_distance():
		
	while True:
		if os.path.isfile(KTREEDIST_OUTPUT):
			break
		time.sleep(1)
		
	with open(KTREEDIST_OUTPUT, 'r') as f:	
		content = f.read()
		regex = re.search("(\d*\.\d+)\s+(\d*\.\d+)", content).group(1)
		distance = float(regex)
		
	return distance
	
def write_output(tree1_path, tree2_path, score, output_name):

	d = {"tree 1": [tree1_path], "tree 2": [tree2_path], "distance": [score]}
	df = pd.DataFrame(d)
	df.to_csv(output_name, sep=',', index=False)

def ktreedist(tree1_file, tree2_file):

	directory = "temp"
	os.makedirs(directory)
	os.chdir(directory)
	
	try:
		t1 = Tree(tree1_file, format = 1)
		t2 = Tree(tree2_file, format = 1)
	except:
		print "file {} or {} was not found".format(tree1_file, tree2_file)	
		sys.exit(0)
	
	unroot_tree.unroot(t1)
	unroot_tree.unroot(t2)
	
	t1.write(outfile = "reference_tree.tree", format = 1)
	t2.write(outfile = "comparison_tree.tree", format = 1)
	
	cmd = "{ktreedist_path} -rt {tree1} -ct {tree2} -t {output}"
	cmd = cmd.format(ktreedist_path = KTREEDIST_CMD, 
						tree1 = "reference_tree.tree", 
						tree2 = "comparison_tree.tree", 
						output = KTREEDIST_OUTPUT)
	
	call(cmd.split(" "))
	
	distance = extract_distance()
	
	os.chdir("../")
	call(["rm", "-rf", directory])

	return distance
	
if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description='')

	parser.add_argument('--reference_tree', '-rt', required=True,
						help='reference tree file')
						
	parser.add_argument('-comparison_tree', '-ct', required=True,
						help='comparison tree file')
						
	parser.add_argument('--output_name', '-o', required=False,
						default="ktreedist_output.csv" , help='output file')
	
	args = parser.parse_args()
	reference_tree = args.reference_tree
	comparison_tree = args.comparison_tree
	output_name = args.output_name

	score = ktreedist(reference_tree, comparison_tree)
	write_output(reference_tree, comparison_tree, score, output_name)