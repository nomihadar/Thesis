from __future__ import division
import os, sys
import argparse
import numpy as np

sys.path.append("/groups/itay_mayrose/nomihadar/code/")

def main(observations_file, maxlength, max_length, pseudocount, output):
	
	observations = list(np.loadtxt(observations_file, 'int'))
	
	lengths = range(1, max(observations)+1)
	counts = [observations.count(length) for length in lengths]
	
	if pseudocount:
		counts = [count + 1 for count in counts]
	
	total = sum(counts)
	probs = [count/total for count in counts]
	
	#limit length
	if maxlength and max_length < len(probs):
		last_prob = sum(probs[max_length-1:])
		probs = probs[:max_length-1] + [last_prob]
	
	#write my lengths model
	np.savetxt(output, probs, '%f')
	
if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--observations_file', '-f', required=True, 
						help='observations file')
	parser.add_argument('--max_length', '-m', type=int, 
						help='max length')
	parser.add_argument('-max', action='store_true', 
						help='limit max')	
	parser.add_argument('--output', '-o', required=False,
						default="",help='output name')
	parser.add_argument('-pseudocount', action='store_true', 
						help='pseudocount')	
	args = parser.parse_args()
	
	main(args.observations_file, args.max, args.max_length, args.pseudocount, args.output)

		
