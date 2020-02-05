import os
import sys
import argparse
import pandas as pd
import numpy as np
import scipy.stats as stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.multicomp import MultiComparison

sys.path.append("/groups/itay_mayrose/nomihadar/code/")

COL_NAME = "distance"

def main(paths_files, output):
	
	with open(paths_files, 'r') as f:
		files = f.read().splitlines()	
	
	values_arr = []	
	
	for i, file in enumerate(files):
		frame = pd.read_csv(file)
		values = frame[COL_NAME]
		values_arr.append(values)
		#data.append(())
	#data = np.rec.array(data)

	statistic, pvalue = stats.f_oneway(*values_arr)
	
	print "anova: "
	print statistic, pvalue
	
	d = {"statistic": [statistic], "pvalue": [pvalue],
		"files": [','.join(files)]}
	df = pd.DataFrame(d)
	df.to_csv(output, sep=',', index=False)
	
	if len(values_arr) < 3:	
		statistic, pvalue = stats.ttest_ind(*values_arr)	
		
		print "ttest: "
		print statistic, pvalue
	
if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='')
	parser.add_argument('-files', required=True,
						help='paths to files')
	parser.add_argument('-o', required=False,
						default="anova_output.csv", help='output')
	args = parser.parse_args()

	main(args.files, args.o)
	