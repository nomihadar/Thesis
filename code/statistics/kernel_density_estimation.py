from __future__ import division
import os, sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KernelDensity
from sklearn.grid_search import GridSearchCV


sys.path.append("/groups/itay_mayrose/nomihadar/code/")

def kde_sklearn(x, x_grid, bandwidth, **kwargs):
	"""Kernel Density Estimation with Scikit-learn"""
	kde_skl = KernelDensity(bandwidth=bandwidth, **kwargs)
	kde_skl.fit(x[:, np.newaxis])
	# score_samples() returns the log-likelihood of the samples
	log_pdf = kde_skl.score_samples(x_grid[:, np.newaxis])
	return np.exp(log_pdf)
	
def estimate_bandwidth(x):
	grid = GridSearchCV(KernelDensity(),
                    {'bandwidth': np.linspace(0.1, 1.0, 30)},
                    cv=20) # 20-fold cross-validation
	grid.fit(x[:, None])
	bandwidth =  grid.best_params_
	
	return bandwidth
	
def main(observations_file, output):
	
	observations = np.loadtxt(observations_file, 'int')
	
	bandwidth = estimate_bandwidth(observations)
	bandwidth = 0.9
	x_grid = np.linspace(1, 100, 1000)
	
	kde_sklearn(observations, x_grid, bandwidth)
	
	# Plot the three kernel density estimates
	fig, ax = plt.figure()
	fig.subplots_adjust(wspace=0)
	

	pdf = kde_sklearn(observations, x_grid, bandwidth)
	ax[1].plot(x_grid, pdf, color='blue', alpha=0.5, lw=3)
	ax[1].hist(observations, ec='gray', fc='gray', alpha=0.4)
	#ax[1].fill(x_grid, pdf_true, ec='gray', fc='gray', alpha=0.4)
	ax[1].set_xlim(1, 100)
	
	plt.savefig("temp.png", dpi=300) 
	
if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--observations_file', '-f', required=True, 
						help='alignment file')
	parser.add_argument('--output', '-o', required=False,
						default="temp",help='output name')	
	args = parser.parse_args()
	
	main(args.observations_file, args.output)

		
