from __future__ import division
import os, sys
import argparse
import numpy as np
import pandas as pd
import scipy.stats as ss
import matplotlib
matplotlib.use('agg')
import seaborn as sns
import matplotlib.pyplot as plt

sys.path.append("/groups/itay_mayrose/nomihadar/code/")
		
MINIMAL_SPECIES = 10

clades = ["magnoliophyta", "rosids", "fabids", "fabaceae"]
ranks = ["order", "family", "subfamily", "tribe", "genus"]

def read_data():

	PATH = '/groups/itay_mayrose/nomihadar/trees/scores/{align}/{based}/{clade}/scores_{group}_{rank}.csv'
	
	alignmens = ["mafft"] #"phlawd"
	based_on = ["cladeSpecific", "magnoMSA"]
	clades = ["magnoliophyta", "rosids", "fabids", "fabaceae"]
	ranks = ["order", "family", "genus"]
	d = {"magnoliophyta": ranks, "rosids":ranks, "fabids":ranks, "fabaceae": ranks[2:]}

	frames = []
	for align in alignmens:
		for j, based in enumerate(based_on):
			for i, clade in enumerate(clades):
				for group in clades[i:]:
				
					for rank in d[group]:
						path = PATH.format(align=align,based=based,
										clade=clade,group=group,rank=rank)
										
						try:
							df = pd.read_csv(path)
						except:
							print(path)
							continue
						df = df[df["num species"] >= MINIMAL_SPECIES]
						df["align"] = align
						df["based"] = based
						df["clade"] = clade
						df["group"] = group
						df["rank"] = rank
						frames.append(df)

	df = pd.concat(frames)
	df.to_csv("scores_data.csv")
	
	return df		

def f(scores):
	return sum([1 for s in scores if s==1]) / len(scores)
	
	
def f(data, align, based, group, rank, ax):
	
	df = data[data["align"] == align]
	d = df[(df["based"] == based) & (df["group"] == group) & 
			(df["rank"] == rank)] 
	'''
	sns.barplot(x="clade", y="scores", data=d, hue="score_type", 
					palette="Set1", ax=ax, 
					order=reversed(clades), hue_order=['score1','score2'], 
					edgecolor=".2", linewidth=1.5)
	'''
	sns.regplot(x="clade", y="scores", data=d,
					palette="Set1", ax=ax, 
					order=reversed(clades),  
					edgecolor=".2", linewidth=1.5)
	
	ax.set(xlabel='', ylabel='')	
	
	return d
		
GROUP = "fabaceae"
RANK = "genus"	

def main(output):
	
	sns.set() #font_scale=1.2
	#sns.set_style("whitegrid")
	
	data = read_data()

	cols = [col for col in list(data) 
			if col != "score1" and col != "score2"]
	data = pd.melt(data, id_vars=cols,
							value_vars=['score2','score1'],
							var_name='score_type', value_name='scores')
	data.to_csv("data.csv")
	
	fig, axarr = plt.subplots(2,1, figsize=(5, 10))

	f(data, "mafft", "cladeSpecific", GROUP, RANK, axarr[0])
	f(data, "mafft", "magnoMSA", GROUP, RANK, axarr[1])
	
	axarr[0].set_title("cladeSpecific   {}/{}".format(GROUP,RANK), loc="left")
	axarr[1].set_title("magnoMSA", loc="left")
	

	axarr[1].legend([],[])
	
	fig.savefig(output, dpi=300)	#, bbox_inches='tight'

	
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='')		
	parser.add_argument('-o', required=False,
						default="plot.png",help='output name')	
	args = parser.parse_args()
	
	main(args.o)
	
	'''
	
	for i, ax in zip(range(2), [ax1, ax2]) :
		for x, tree in zip(range(3), trees):
			for x_pos, rank in zip([x-0.3,x,x+0.3],ranks):
				
				grouped = grouped_arr[i]
				median = grouped.median()[tree][rank]
				size = grouped.size()[tree][rank]
				
				mono = grouped.apply(f)[tree][rank]
				
				if i == 0:
					if tree=="Zanne" and rank=='family':
						y_pos = 0.87
					elif tree=="Zanne" and rank=='order':
						y_pos = 0.82
					elif tree=="PHLAWD" and rank=='order':
						y_pos = 0.05
					elif tree=="Mafft" and rank=='order':
						y_pos = 0.07
					else:
						y_pos = median-0.04
				else:
					if tree=="Zanne" and rank=='family':
						y_pos = 0.9
					elif tree=="Zanne" and rank=='order':
						y_pos = 0.9
					else:
						y_pos = median-0.04
				
				ax.text(x_pos, y_pos, "{:0.2f}".format(mono), 
						horizontalalignment='center', 
						size='x-small', color='black', weight='semibold')
	
	'''
