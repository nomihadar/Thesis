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

PATHS = {"Zanne": {"order": "/groups/itay_mayrose/nomihadar/articles/Zanne/scores/scores_magnoliophyta_order.csv", 
			"family": "/groups/itay_mayrose/nomihadar/articles/Zanne/scores/scores_magnoliophyta_family.csv",
			"genus": "/groups/itay_mayrose/nomihadar/articles/Zanne/scores/scores_magnoliophyta_genus.csv"},#zanne tree
			
		#my tree phlawd	
		"PHLAWD": {"order": "/groups/itay_mayrose/nomihadar/trees/magnoliophyta_tree/sequences_filtered_zanne/tree_phlawd_scores/scores_magnoliophyta_order.csv", 
			"family": "/groups/itay_mayrose/nomihadar/trees/magnoliophyta_tree/sequences_filtered_zanne/tree_phlawd_scores/scores_magnoliophyta_family.csv",
			"genus": "/groups/itay_mayrose/nomihadar/trees/magnoliophyta_tree/sequences_filtered_zanne/tree_phlawd_scores/scores_magnoliophyta_genus.csv"},
		
		#my tree mafft
		"MAFFT": {"order": "/groups/itay_mayrose/nomihadar/trees/magnoliophyta_tree/sequences_filtered_zanne/tree_mafft_scores/scores_magnoliophyta_order.csv", 
			"family": "/groups/itay_mayrose/nomihadar/trees/magnoliophyta_tree/sequences_filtered_zanne/tree_mafft_scores/scores_magnoliophyta_family.csv",
			"genus": "/groups/itay_mayrose/nomihadar/trees/magnoliophyta_tree/sequences_filtered_zanne/tree_mafft_scores/scores_magnoliophyta_genus.csv"}			
		}
		
MINIMAL_SPECIES = 10

def read_data():

	frames = []
	for tree in ["Zanne", "PHLAWD", "MAFFT"]:
		for rank in ['genus', 'family', 'order']:
			df = pd.read_csv(PATHS[tree][rank])
			df = df[df["num species"] >= MINIMAL_SPECIES]
			df["rank"] = rank
			df["tree"] = tree
			frames.append(df)
		
		'''
		new_frames = []
		for num in [10, 50, 100, 500, 1000]:
			col_name = 'num species'
			df1 = df[df[col_name] >= num]
			df1[col_name] = ">{}".format(num)
			new_frames.append(df1)
		df = pd.concat(new_frames)
		final.apend(df)		
		'''
	df = pd.concat(frames)
	df.to_csv("scores_data.csv")
	
	return df		

def f(scores):
	return sum([1 for s in scores if s==1]) / len(scores)

def main2():
	
	sns.set(font_scale=1.5)
	#sns.set_style("whitegrid")
	
	data = read_data()

	fig, axarr = plt.subplots(2,2, figsize=(12, 10))
	ax0 = axarr[0,0]
	ax1 = axarr[1,0]
	ax2 = axarr[1,1]
	
	ax0.set_title("A", loc="left")
	ax1.set_title("B", loc="left")
	ax2.set_title("C", loc="left")
	
	boxes = sns.boxplot(x="tree", y="score1", hue="rank", data=data, 
				palette="Set1", ax=ax1,  width=0.9)
	ax1.set(xlabel='', ylabel='score 1')
	
	sns.boxplot(x="tree", y="score2", hue="rank", data=data, 
				palette="Set1", ax=ax2,  width=0.9)
	ax2.set(xlabel='', ylabel='score 2')
	
	grouped1 = data.groupby(['tree','rank'])['score1']
	grouped2 = data.groupby(['tree','rank'])['score2']
	#print (grouped1.size())
	
	mono = grouped1.apply(f).reset_index(name="monophyly percent")
	
	trees = ["Zanne", "PHLAWD", "Mafft"]
	ranks = ['genus', 'family', 'order']
	
	sns.barplot(x="tree", y="monophyly percent", hue="rank", data=mono, 
					palette="Set1", ax=ax0, order=trees, hue_order= ranks, 
					edgecolor=".2", linewidth=2.0)
	ax0.set(xlabel='', ylabel='percent')
	

	for ax in [ax0, ax1, ax2]:
		ax.legend([],[])
	
	handles, labels = ax0.get_legend_handles_labels()
	labels = ['Genus (n=528)', 'Family (n=205)', 'Order (n=51)']
	plt.legend(handles, labels, bbox_to_anchor=(0.01, 2.2), 
				loc=2, borderaxespad=0., fontsize=14)
	axarr[0,1].axis('off')
	
	fig.savefig("output_avg.png", dpi=300, bbox_inches='tight')	

def main(output):
	
	sns.set(font_scale=1.5)
	#sns.set_style("whitegrid")
	
	data = read_data()

	fig, axarr = plt.subplots(2,2, figsize=(12, 10))
	ax0 = axarr[0,0]
	ax1 = axarr[1,0]
	ax2 = axarr[1,1]
	
	ax0.set_title("A", loc="left")
	ax1.set_title("B", loc="left")
	ax2.set_title("C", loc="left")
	
	grouped1 = data.groupby(['tree','rank'])['score1']
	grouped2 = data.groupby(['tree','rank'])['score2']
	#print (grouped1.size())
	
	mono = grouped1.apply(f).reset_index(name="percent")
	
	trees = ["Zanne", "PHLAWD", "MAFFT"]
	ranks = ['genus', 'family', 'order']
	
	sns.barplot(x="tree", y="percent", hue="rank", data=mono, 
					palette="Set1", ax=ax0, order=trees, hue_order= ranks, 
					edgecolor=".2", linewidth=1.5)
	ax0.set(xlabel='', ylabel='percent')
	
	boxes = sns.barplot(x="tree", y="score1", hue="rank", data=data, 
						palette="Set1", ax=ax1, order=trees,
						edgecolor=".2", linewidth=1.5)
	ax1.set(xlabel='', ylabel='score 1')
	
	sns.barplot(x="tree", y="score2", hue="rank", data=data, 
				palette="Set1", ax=ax2, order=trees,
				edgecolor=".2", linewidth=1.5)
	ax2.set(xlabel='', ylabel='score 2')
	
	for ax in [ax0, ax1, ax2]:
		ax.legend([],[])
	
	handles, labels = ax0.get_legend_handles_labels()
	labels = ['Genus (n=528)', 'Family (n=205)', 'Order (n=51)']
	plt.legend(handles, labels, bbox_to_anchor=(0.01, 2.2), 
				loc=2, borderaxespad=0., fontsize=14)
	axarr[0,1].axis('off')
	
	fig.savefig(output, dpi=300, bbox_inches='tight')	

	
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
