from __future__ import division
import os, sys
import argparse
import numpy as np
import pandas as pd
from scipy import stats, special  
from scipy.stats import zipf
from scipy.stats import nbinom

sys.path.append("/groups/itay_mayrose/nomihadar/code/")

MIN_BIN = 5
MAX_R_VALUE = 51

def write_output(df, output, output2):
	
	#df = df.round(4)
	df = df.sort_values(["2pvalue", "1chisq"], ascending=[False,True])
	df.to_csv(output, sep=',', index=False)
	
	if df.shape[0] > 1:
		first_row = df[0:1]
		first_row.to_csv(output2, sep=',', index=False)	

def get_shape_values(shape_file, dist):

	if dist == "zipf":
		
		if os.path.isfile(shape_file):
			a_values = pd.read_csv(shape_file)
			a_values = [a_values["a"][0]]
		else:
			a_values = np.linspace(1.0001, 2, 1000)

		return a_values 
		
	elif dist == "negbinom":
	
		if os.path.isfile(shape_file):
			shape_values = pd.read_csv(shape_file)
			r_values = [shape_values["r"][0]]
			p_values = [shape_values["p"][0]]		
		else:
			r_values = range(1,MAX_R_VALUE)
			p_values = np.linspace(0.0000001, 1, 1000, endpoint=False)
			
			shape_values = []
			for r in r_values:
				for p in p_values:
					shape_values.append((r,p))
			
		return shape_values 
	
def user_distribution(observations, min_prob, maxlength, dist_file):
	
	max_length = maxlength if maxlength else max(observations)
	
	#remove observations larger than the maximal length
	observed = [o for o in observations if o <= max_length]

	#define results data frame

	results = { "1chisq": [], "2pvalue": [], 
				"3n.observations": [], "4n.bins": [], 
				"5n.expected < 5": [], "6n.observed < 5": []}
				
	#get user distribution 
	user_dist = pd.read_csv(dist_file)
	occurrences = user_dist["occurrences"].values[:max_length]
	
	expect_freq = np.array(occurrences) / sum(occurrences)
	
	# accumulate frequencies to a minimal probability of MIN_PROB 
	acc_freqs = [0]
	bins_lengths = [0]
	for freq in expect_freq:
		if acc_freqs[-1] < min_prob:
			acc_freqs[-1] += freq
			bins_lengths[-1] += 1
		else:
			acc_freqs.append(freq)
			bins_lengths.append(1)

	acc_expected = np.array(acc_freqs) * len(observed)
	
	#observed:
	observed_hist = list(np.bincount(observed)[1:])
	
	# accumulate observations according to the accumulated frequencies
	i = 0
	acc_observed = []
	for length in bins_lengths:	
		acc_observed.append(sum(observed_hist[i:i+length]))
		i += length
	
	try:
		chisq, pval = stats.chisquare(acc_observed, acc_expected)
	except:
		chisq, pval = -1, -1
	
	#count how many bins are less than 5 in both expected and observed 
	less_obs = sum(i < MIN_BIN for i in acc_observed)
	less_exp = sum(i < MIN_BIN for i in acc_expected)
	
	results["1chisq"].append(chisq) 
	results["2pvalue"].append(pval)
	results["3n.observations"].append(len(observed)) 
	results["4n.bins"].append(len(acc_expected))
	results["5n.expected < 5"].append(less_exp)
	results["6n.observed < 5"].append(less_obs)
	
	return pd.DataFrame(results)
	
def chisquare(observations, shape_file, min_prob, maxlength, dist):
	
	max_length = maxlength if maxlength else max(observations)
	
	'''
	if not maxlength or (maxlength and max(observations) < maxlength):
		max_length = max(observations)
	else:
		max_length = maxlength
	'''
		
	#remove observations larger than the maximal length
	observed = [o for o in observations if o <= max_length]
	
	#get shape parameters 
	shape_values = get_shape_values(shape_file, dist)

	#define results data frame
	
	results = {"0shape": [], "1chisq": [], "2pvalue": [], 
				"3n.observations": [], "4n.bins": [], 
				"5n.expected < 5": [], "6n.observed < 5": []}	
	
	if dist == "negbinom":
		results["0shape2"] = []
	
	for shape in shape_values:
		
		#calculate expected frequencies:
		if dist == "zipf":
			expect_freq = zipf.pmf(range(1,max_length+1), shape) 
		elif dist == "negbinom":
			r, p = shape
			expect_freq = nbinom.pmf(range(1,max_length+1), r, p) 

		try:
			expect_freq = np.array(expect_freq) / sum(expect_freq)
		except:
			print ("shape caused zero-division: ", shape)
			
		# accumulate frequencies to a minimal probability of MIN_PROB 
		acc_freqs = [0]
		bins_lengths = [0]
		for freq in expect_freq:
			if acc_freqs[-1] < min_prob:
				acc_freqs[-1] += freq
				bins_lengths[-1] += 1
			else:
				acc_freqs.append(freq)
				bins_lengths.append(1)

		acc_expected = np.array(acc_freqs) * len(observed)
		
		#observed:
		observed_hist = list(np.bincount(observed)[1:])
		
		# accumulate observations according to the accumulated frequencies
		i = 0
		acc_observed = []
		for length in bins_lengths:	
			acc_observed.append(sum(observed_hist[i:i+length]))
			i += length
			
		try:
			chisq, pval = stats.chisquare(acc_observed, acc_expected)
		except:
			chisq, pval = -1, -1
		
		'''
		print bins_lengths
		print expect_freq
		print max_length
		print observed_hist
		print acc_observed	
		print acc_expected	
		'''
		
		#count how many bins are less than 5 in both expected and observed 
		less_obs = sum(i < MIN_BIN for i in acc_observed)
		less_exp = sum(i < MIN_BIN for i in acc_expected)
		if dist == "zipf":
			results["0shape"].append(shape)
		if dist == "negbinom":
			results["0shape"].append(r)	
			results["0shape2"].append(p)
		results["1chisq"].append(chisq) 
		results["2pvalue"].append(pval)
		results["3n.observations"].append(len(observed)) 
		results["4n.bins"].append(len(acc_expected))
		results["5n.expected < 5"].append(less_exp)
		results["6n.observed < 5"].append(less_obs)
		
	return pd.DataFrame(results)
		
def read(path):
	data = np.loadtxt(path, 'int', ndmin=1)
	return data	
	
def concat_observations(files):
	
	with open(files, 'r') as f:
		paths = f.read().splitlines()
	observations = []
	for path in paths:
		obs = read(path)
		observations.extend(obs)			
	return observations		
	
def write_mean(final, output):	
	d = {}
	for column in final.iloc[:,:-1]:
		d[column + " std"] = [final[column].std()]
		d[column + " avg"] = [final[column].mean()]
	df = pd.DataFrame(d)
	df.to_csv(output, index=False)
		
def main(observations_file, dist, output, output2, output3,
		shape_file, min_prob, paths, maxlength, concat):

	if paths:
		with open(observations_file, 'r') as f:
			paths = f.read().splitlines()
			
		frames = []
		for path in paths:
			observations = np.loadtxt(path, 'int', ndmin=1)
			if not len(observations):
				print "empty file: ", path
				continue
				
			df = chisquare(observations, shape_file, min_prob, maxlength, dist)
			
			df['path'] = [path]
			frames.append(df)	
		if not frames:
			print "lack :", observations_file
			exit(0)
		else:	
			final = pd.concat(frames)
			write_mean(final, output2)
	
	else:
		if concat:
			observations = concat_observations(observations_file)
		else:
			observations = np.loadtxt(observations_file, 'int', ndmin=1)
		
		#final = chisquare(observations, shape_file, min_prob, maxlength, dist)
		final = user_distribution(observations, min_prob, maxlength, dist)
	
	write_output(final, output, output3)
		
if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--observations_file', '-f', required=True, 
						help='alignment file')
	parser.add_argument('--output', '-o', required=False,
						default="chisquare_test.csv",help='output name')
	parser.add_argument('--output2', '-o2', required=False,
						default="chisquare_test_mean.csv",help='output name')
	parser.add_argument('--output3', '-o3', required=False,
						default="maximal_p-value.csv",help='output name')
	parser.add_argument('--dist', '-d', required=False,
						help='distribution')
	parser.add_argument('--min_prob', '-p', required=False,type=float,
						help='minimal probability in a bin, should be a float')
	parser.add_argument('-params_file', required=False, 
						default=" ", help='parameter file')	
	parser.add_argument('-paths', action='store_true', 
						help='file contains paths')	
	parser.add_argument('-maxlength', type=int,
						default=0, help='max length observation')
	parser.add_argument('-concat', action='store_true',
						help="concatenate all observations in paths file")
	args = parser.parse_args()
	
	main(args.observations_file, args.dist, args.output, args.output2, args.output3,
		args.params_file, args.min_prob, args.paths, args.maxlength, args.concat)
	
	