import os
import time
import sys
import re
import numpy as np
import logging
import argparse
	
def extract_distance():
		
	while True:
		if os.path.isfile("outfile"):
			break
		time.sleep(2)
		
	with open("outfile",'r') as f:	
		content = f.read()
		regex = re.search("Tree pair 1:\s+(.*)", content).group(1)
		distance = float(regex)
	
	return distance
		
def treedist(tree1_path, tree2_path):
	
	directory = "temp"

	os.system("mkdir " + directory)
	os.system("cp " + tree1_path + " " + directory + "/intree")
	os.system("cp " + tree2_path + " " + directory + "/intree2")
	os.chdir(directory)
	
	#Branch Score Distance
	os.system('echo "2\nC\nV\nY\n" | treedist')
	branch_score = extract_distance()
	os.system("rm " + "outfile")
	
	#Symmetric Difference (robinson fold)
	os.system('echo "D\n2\nC\nV\nY\n" | treedist')
	symmetric_differ = extract_distance()
	
	os.chdir("../")
	os.system("rm -rf " + directory)
	
	d = {}
	d["bs"] = branch_score
	d["rf"] = symmetric_differ
	
	return d
	
def write_output(tree1_path, tree2_path, scores):

	with open("treedist.output",'w') as f:
		f.write("tree 1: {}\n".format(tree1_path)) 
		f.write("tree 2: {}\n".format(tree2_path)) 
		f.write("RF distance : {}\n".format(scores["rf"])) 
		f.write("Branch score distance : {}\n".format(scores["bs"]))	
	
	
if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='')

	parser.add_argument('--tree1', '-t1', required=True,
						, help='tree1 file')
						
	parser.add_argument('--tree2', '-t2', required=True,
						, help='tree2 file')
	
	args = parser.parse_args()
	tree1_file = args.tree1
	tree2_file = args.tree1

	score = treedist(tree1_file, tree2_file)
	write_output(tree1_file, tree2_file, score)