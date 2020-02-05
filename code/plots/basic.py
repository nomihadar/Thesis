import os, sys
import argparse
import pandas as pd
import matplotlib 
matplotlib.use('agg')
import seaborn as sns
import matplotlib.pyplot as plt

sys.path.append("/groups/itay_mayrose/nomihadar/code/")


def main(output):
	
	d1 = get_lengths(DATA1)
	d2 = get_lengths(DATA2)
	d3 = get_lengths(DATA3)
	d4 = get_lengths(DATA4)

	sns.set(font_scale=1.5)
	#sns.set_style("whitegrid")
	
	fig, axarr = plt.subplots(2,2, figsize=(10, 10))
	
	sns.distplot(d1, kde=False, rug=False, ax=axarr[0,0], hist_kws=dict(alpha=1), color="#6897bb")
	sns.distplot(d2, kde=False, rug=False, ax=axarr[0,1], hist_kws=dict(alpha=1),color="#ffa500")
	sns.distplot(d3, kde=False, rug=False, ax=axarr[1,0], hist_kws=dict(alpha=1),color="#6897bb")
	sns.distplot(d4, kde=False, rug=False, ax=axarr[1,1], hist_kws=dict(alpha=1),color="#ffa500")
	
	axarr[1,0].set_xlabel('Sequences length')
	axarr[1,1].set_xlabel('Sequences length')
	
	axarr[0,0].set_ylabel('Count')
	axarr[1,0].set_ylabel('Count')

	
	fig.savefig(output, dpi=300, bbox_inches='tight')	
	
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='')		
	parser.add_argument('-o', required=False,
						default="plot.png",help='output name')	
	args = parser.parse_args()
	
	main(args.o)