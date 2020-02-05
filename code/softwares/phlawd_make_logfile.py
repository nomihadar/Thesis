"""
Goal: 		create a summerized logfile from all logfiles created by each	
			run of PHLAWD
Input args: root - a path for the phlawd outputs 
Author:		Nomi Hadar
Date:		April 2016
"""
import csv
import os
import sys

LOGFILE_NAME = "my_phlawd_logfile"


def count_species_in_alignment(root):
	
	d = {} #key = gene, value = num species 
	no_align = [] #name of genes with error in alignment
	
	#for each dir 
	for dir in os.listdir(root):
		
		#if not a dir - continue
		if not os.path.isdir(os.path.join(root,dir)):
			continue
			
		#name of dir is a gene
		gene = dir
	
		#iterate over files in directory
		files = os.listdir(os.path.join(root,dir))
		
		#if the folder is empty 
		if not files:
			pass
		
		file_exists = False
		for file in files:
		
			#path of current file 
			file_path = os.path.join(root,dir,file)
			
			#if current file is the logfile 
			if file.endswith(".FINAL.aln"):
				file_exists = True
				
				with open(file_path, 'r') as fout:
					lines = fout.readlines()
					num_species = sum([row.count('>') for row in lines])
					d[gene] = num_species
	
		if not file_exists:
			no_align.append(gene)
	
	return (d, no_align)
					

def write_output(d, no_align):

	out_path = os.path.join(root, LOGFILE_NAME)

	with open(out_path, 'w') as fout:
		
		fout.write("gene,number of species\n")
		for gene, num_species in d.iteritems():
			row = '{gene},{num}\n'.format(gene = gene, num = str(num_species))
			fout.write(row)
		
		if no_align:
			fout.write("\nsome errors in the following genes:\n") 
			for gene in no_align:
				row = "{gene}\n".format(gene = gene)
				fout.write(row)
	

if __name__ == "__main__":

	if len(sys.argv) < 2:
		print "please insert arguments"
		sys.exit(0)
		
	#get the path for the output dit
	root = sys.argv[1]	

	(d, no_align) = count_species_in_alignment(root)

	write_output(d, no_align)
