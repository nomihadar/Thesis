# example: python convert_formats.py input_alignment output_file fasta phylip-relaxed
import argparse
import sys
import os
from Bio import AlignIO

sys.path.append("/groups/itay_mayrose/nomihadar/code/")

def convert(input_path, output_path, current_format, convert_to):
	print input_path
	input_handle = open(input_path, "rU")
	output_handle = open(output_path, "w")

	alignments = AlignIO.parse(input_handle, current_format)
	AlignIO.write(alignments, output_handle, convert_to)

	output_handle.close()
	input_handle.close()	

def paths(input, output, current_format, convert_to):

	with open(input, 'r') as f:
		paths = f.read().splitlines()
		
	for path in paths:
		output_path = "{}.{}".format(os.path.basename(path).split(".")[0], 
									convert_to)
		convert(path, output_path, current_format, convert_to)
	
if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--input_path', '-in', help='path to input file')
	parser.add_argument('--output_path', '-out', help='output name', 
						default="converted")
	parser.add_argument('--current_format', '-f', help='current format')
	parser.add_argument('--convert_to', '-newf', help='new format')
	parser.add_argument('-paths', action='store_true', 
						help='file contains paths')
	args = parser.parse_args()
	
	if args.paths:
		paths(args.input_path, args.output_path, 
				args.current_format, args.convert_to)
	else:
		convert(args.input_path, args.output_path, 
				args.current_format, args.convert_to)