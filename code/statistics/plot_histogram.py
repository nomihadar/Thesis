from __future__ import division
import os, sys
import argparse
import numpy as np
import pandas as pd
import scipy.stats as ss
import matplotlib
matplotlib.use('agg')
import seaborn 
import matplotlib.pyplot as plt


sys.path.append("/groups/itay_mayrose/nomihadar/code/")

TITLE = "Histogram of indels lengths"
MAX = 100

def concat_observations(files):
	
	with open(files, 'r') as f:
		paths = f.read().splitlines()
	observations = []
	for path in paths:
		obs = np.loadtxt(path, 'int', ndmin=1)
		observations.extend(obs)			
	return observations		

def create_histogram(observations_file, output, concat):
	
	#load observations
	if concat:
		observations = concat_observations(observations_file)
	else:
		observations = np.loadtxt(observations_file, 'int')
	
	#define bins
	max_obs = MAX if MAX < max(observations) else max(observations)
	bins = np.arange(1,max_obs+1)
	
	#create a new figure 
	fig = plt.figure()
	ax = fig.add_subplot(111)
	
	#plot histogram
	n, bins, patches = plt.hist(np.clip(observations, 1, bins[-1]),
								bins=bins, normed=True)
	
	#change last label to num+
	if max(observations) > MAX:
		labels = ax.get_xticks().tolist()
		labels[-1]= '{}+'.format(labels[-1])
		ax.set_xticklabels(labels)
	
	#add text
	ymin, ymax = ax.get_ylim()
	xmin, xmax = ax.get_xlim()
	num_observation = "# observs: {}".format(len(observations))
	ax.text(xmax*0.1, ymax*0.90, num_observation)
	
	#add titles 
	plt.xlim(xmin= 1, xmax=max_obs+1)
	plt.title("{}".format(TITLE), fontsize=14, fontweight='bold')
	plt.xlabel("indels lengths", fontweight='bold')
	plt.ylabel("frequency", fontweight='bold')
	plt.savefig(output, dpi=100)
	
if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--observations_file', '-f', required=True, 
						help='alignment file')
	parser.add_argument('-concat', action='store_true',
						help="concatenate all observations in paths file")
	
	parser.add_argument('--output', '-o', required=False,
						default="plot.png",help='output name')	

	args = parser.parse_args()

	create_histogram(args.observations_file, args.output, args.concat)