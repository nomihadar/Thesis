import os, sys
import argparse
import pandas as pd

sys.path.append("/groups/itay_mayrose/nomihadar/code/")

INDEL_DIR = "indels_files"
INDEL_FILE = "chosen_indels.csv"

def collect_indels(root, output):

	indel_dir = os.path.join(root, INDEL_DIR)
	frames = []
	for dir in os.listdir(indel_dir):
		path = os.path.join(indel_dir, dir, INDEL_FILE)
		frame = pd.read_csv(path)
		frame['block'] = [dir]
		frames.append(frame)
	
	final = pd.concat(frames)
	final.index = [root] * len(final)
	
	final = pd.concat(frames)
	final.to_csv(output, index=False)

	
if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--root', '-r', help='directory')
	parser.add_argument('--output', '-o', help='output')
	args = parser.parse_args()
	
	collect_indels(args.root, args.output)
	
	