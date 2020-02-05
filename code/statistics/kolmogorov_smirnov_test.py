from __future__ import division
import os, sys
import argparse
import numpy as np
import pandas as pd
from scipy import stats, special  
from scipy.stats import zipf
from scipy.stats import nbinom

sys.path.append("/groups/itay_mayrose/nomihadar/code/")

def write_output(dic, output):
	df = pd.DataFrame(dic)
	df = df.sort_values("p-value", ascending=False)
	df.to_csv(output, sep=',', index=False)
	
	if df.shape[0] > 1:
		first_row = df[0:1]
		first_row.to_csv("maximal_p-value.csv", sep=',', index=False)	

def nbinom(observations_file, output, params_file):
	
	obs = np.loadtxt(observations_file, 'int')

	if os.path.isfile(params_file):
		r_values = [pd.read_csv(params_file)["r"][0]]
		p_values = [pd.read_csv(params_file)["p"][0]]
	else:
		r_values = range(1, 1000)
		p_values = np.linspace(0.00001, 1, 1000)
	
	results = {"1r": [], "2p": [], "3D": [], "p-value": []}
	for r in r_values:
		for p in p_values:
			d, p_val = stats.kstest(obs, 'nbinom', args = (r,p,))
			results["1r"].append(r) 
			results["2p"].append(p) 
			results["3D"].append(d) 
			results["p-value"].append(p_val) 
	
	write_output(results, output)	
			
def zip_cdf(x_arr, a, max_obs):
	#print x_arr
	result = []
	for x in x_arr:
		if x <= max_obs:
			result.append( zipf.cdf(x, a) / zipf.cdf(max_obs, a))
	#print result
	return result
	
def zipf_cut_tail(observed, output, a_file, maxlength):

	max_obs = maxlength if maxlength else max(observed)
	
	#distribution parameter - a 
	if os.path.isfile(a_file):
		a_values = pd.read_csv(a_file)
		a_values = [a_values["a"][0]]
	else:
		a_values = np.linspace(1.0001, 2, 100000)

	results = {"1a": [], "2D": [], "p-value": []}
	for a in a_values:
		
		#d, p = stats.kstest(obs, 'zipf', args = (a,))
		
		d, p = stats.kstest(observed, lambda x: zip_cdf(x, a, max_obs))
		results["1a"].append(a) 
		results["2D"].append(d) 
		results["p-value"].append(p) 
	
	return pd.DataFrame(results)

def concat_observations(files, paths):

	if not paths:
		observations = read(files)
	else:
		with open(files, 'r') as f:
			paths = f.read().splitlines()
		
		observations = []
		for path in paths:
			obs = read(path)
			observations.extend(obs)
					
	return observations		
	
def main(observations_file, dist, output, output2, 
		params_file, paths, maxlength):

	if paths:
		with open(observations_file, 'r') as f:
			paths = f.read().splitlines()
		frames = []
		for path in paths:
			observations = np.loadtxt(path, 'int', ndmin=1)
			df = zipf_cut_tail(observations, output, params_file, maxlength)
			df['path'] = [path]
			frames.append(df)
			
		final = pd.concat(frames)
		
		d = {}
		for column in final.iloc[:,:-1]:
			d[column + " std"] = [final[column].std()]
			d[column + " avg"] = [final[column].mean()]
		df = pd.DataFrame(d)
		df.to_csv(output2, index=False)
		
	else:
		observations = np.loadtxt(observations_file, 'int', ndmin=1)
		final = zipf_cut_tail(observations, output, params_file, maxlength)
	
	write_output(final, output)

	
if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--observations_file', '-f', required=True, 
						help='alignment file')
	parser.add_argument('--output', '-o', required=False,
						default="ks_test",help='output name')
	parser.add_argument('--output2', '-o2', required=False,
						default="ks_test_mean.csv",help='output name')
	parser.add_argument('--dist', '-d', required=False,
						help='distribution')
	parser.add_argument('-params_file', required=False, 
						default=" ", help='parameter file')	
	parser.add_argument('-paths', action='store_true', 
						help='file contains paths')	
	parser.add_argument('-maxlength', type=int,
						default=0, help='max length observation')
	args = parser.parse_args()
	
	main(args.observations_file, args.dist, args.output, args.output2,
		args.params_file, args.paths, args.maxlength)

		
