"""
Goal: 		concatenate aligments
Input args: a path to a file with list of paths to MSAa
Author:		Nomi Hadar
Date:		April 2016
"""
import datetime
import sys
import os
from subprocess import call

#the path to the perl script which concate alignments
CONCATE_SCRIPT_PATH = "/groups/pupko/haim/pupkoSVN/trunk/programs/indelReliability/ConcateAlignments.pl"

CONCATE_CMD = "perl {script_path} {MSAs_ls} {output_name} {logile_name} NO NA NA"

OUTPUT_FILE = "concat_output.fasta"
TEMP_OUTPUT_FILE = "concat_output_TEMP.fasta"
LOGFILE = "concat_logfile.txt"

#name of the file which is the input to the concatenate step 
MSAs_LS_FILE = "list_of_paths_of_MSAs"

def concatenate(MSAs_list):
	
	concat_align_cmd = CONCATE_CMD.format (script_path = CONCATE_SCRIPT_PATH, 
						MSAs_ls = MSAs_list, 
						output_name = TEMP_OUTPUT_FILE, 
						logile_name = LOGFILE)
	#print concat_align_cmd
	call(concat_align_cmd.split(" "))
	
	with open(TEMP_OUTPUT_FILE) as infile:
		with open(OUTPUT_FILE, 'w') as outfile:
			for line in infile:
				line = line.replace("?", "-")
				outfile.write(line)

if __name__ == "__main__":

	if len(sys.argv) < 2:
		print "please insert argument"
		sys.exit(0)
		
	#get a path to file of list of paths to MSAs files 
	file_path = sys.argv[1]
	concatenate(file_path)

		