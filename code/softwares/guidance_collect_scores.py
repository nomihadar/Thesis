import os, sys
import argparse, re
import pandas as pd
from subprocess import call
import numpy as np

sys.path.append("/groups/itay_mayrose/nomihadar/code/")
 
import create_paths_list as create_paths

SCORES_FILE = "MSA.MAFFT.Guidance2_msa.scr"
LOG_FILE = "log"
OUTPUT = "guidance_scores.csv"
OUTPUT_MEANS = "guidance_scores_means.csv"

def extract_seq_file(path):
	guidance_dir = os.path.dirname(path)
	path = os.path.join(guidance_dir, LOG_FILE)
	#guidance_output_dir
	with open(path, 'r') as f:
		content = f.read()
		seq_file = re.search(r'--seqFile\s+(\S+)', content).group(1)
	
	return seq_file

def extract_scores(path):

	#guidance_output_dir
	with open(path, 'r') as f:
		content = f.read()
		rows = re.search(r'ROWS\s+(\d+)', content).group(1)
		cols = re.search(r'COLUMNS\s+(\d+)', content).group(1)
		pair_score = re.search(r'PAIR_SCORE\s+(\d+\.\d+)', content).group(1)
		col_score = re.search(r'COL_SCORE\s+(\d+\.\d+)', content).group(1)
	
	seq_file = extract_seq_file(path)
	seq_file_name = os.path.basename(seq_file)
	#create a data frame
	columns = ['# rows', '# columns', 
				'pair score', 'column score', 'seq file']
	data = [[int(rows), int(cols), 
			float(pair_score), float(col_score), seq_file]]
	df = pd.DataFrame(data, columns=columns, index=[seq_file_name])
	
	return df

def main_paths(paths_file):

	#get input list_path
	with open(paths_file, 'r') as f:
		score_files = f.read().splitlines()
	
	frames = []
	for score_file in score_files:
		df = extract_scores(score_file)
		frames.append(df)
		
	final = pd.concat(frames)
	final.to_csv(OUTPUT)
	
	#compute means
	means = {column: [final[column].mean()] 
					for column in final.iloc[:,:-1]}
	means['# scores'] = len(final)
	means['sd column score'] = np.std(final['column score'])
	means = pd.DataFrame(means)

	#reorder names 
	#cols = means.columns.tolist()
	#cols = [cols[2]] + cols[:2] + cols[3:]
	#means = means[cols]

	#means = pd.DataFrame(means)
	means.to_csv(OUTPUT_MEANS, index=False)
	
def main(scores_file):	
	df = extract_scores(scores_file)
	df.to_csv(OUTPUT)
	
if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--score_file', '-f', required=False,
						help='path to score file')
	parser.add_argument('-paths', action='store_true',
						help='file cntains files paths')
	parser.add_argument('-root', action='store_true', 
						help='root contains sequences file')
	args = parser.parse_args()
	
	if args.paths:
		main_paths(args.score_file)
	elif args.root:
		create_paths.main(args.score_file, "msa.scr")
		main_paths("paths.txt")
	else:
		main(args.score_file)
	
	