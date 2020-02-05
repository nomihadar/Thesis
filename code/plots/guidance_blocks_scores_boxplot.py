import os, sys
import argparse
import pandas as pd
import matplotlib 
matplotlib.use('agg')
import seaborn as sns
import matplotlib.pyplot as plt

sys.path.append("/groups/itay_mayrose/nomihadar/code/")

X = "gene"
Y = "column score" 
TYPE = "type"
NOT_REMOVE = "not removed"
REMOVE = "remove"

#goup = reference/ simulation

GENES = ['18S', '26S', 'ITS', 'atpB', 'matK', 'rbcL', 'trnLtrnF']

OPTIMIM_LARGE = "/groups/itay_mayrose/nomihadar/simulations/dataset_big/sim_sequences/3guidance/mymethod2018/scores/{}/guidance_scores.csv"
OPTIMIM_SMALL = "/groups/itay_mayrose/nomihadar/simulations/dataset_small/sim_sequences/3guidance/mymethod2018/scores/{}/guidance_scores.csv"

REMOVE_LARGE = "/groups/itay_mayrose/nomihadar/simulations/dataset_big/sim_sequences/7remove_edges/guidance/scores/{}/guidance_scores.csv"
REMOVE_SMALL = 


def create_data(ref_path, optimim_path, sparta_path, output):
	
	optimim = [(gene, OPTIMIM, optimim_path.format(gene)) for gene in GENES]
	sparta = [(gene, SPARTA, sparta_path.format(gene)) for gene in GENES]
	sim = optimim + sparta
	
	frames = []
	for gene, type, path in sim:
		
		df = pd.read_csv(path)
		df = df[[Y]]
		
		df[X] = gene
		df[TYPE] = type
		
		frames.append(df)
	
	df = pd.read_csv(ref_path)
	df = df[[Y, X]]
	df[TYPE] = REFERENCE
	frames.append(df)
	
	df = pd.concat(frames)
	df.to_csv(output)

	return df

def set_edge_color(ax):
	for i, artist in enumerate(ax.artists):
		# Set the linecolor on the artist to the facecolor, and set the facecolor to None
		col = artist.get_facecolor()
		artist.set_edgecolor(col)
		artist.set_facecolor('None')
		
		# Each box has 6 associated Line2D objects (to make the whiskers, fliers, etc.)
		# Loop over them here, and use the same colour as above
		for j in range(i*6,i*6+6):
			line = ax.lines[j]
			line.set_color(col)
			line.set_mfc(col)
			line.set_mec(col)
				

	
def main(output):
	
	data_large = create_data(REF_LARGE, OPTIMIM_LARGE, SPARTA_LARGE, "large.csv")
	data_small = create_data(REF_SMALL, OPTIMIM_SMALL, SPARTA_SMALL, "small.csv")

	sns.set(font_scale=1.2)
	#sns.set_style("whitegrid")
	
	fig, axarr = plt.subplots(2,1, figsize=(10, 9), sharex=False)

	hue_order = [REFERENCE, SPARTA, OPTIMIM]
	
	sns.boxplot(x=X, y=Y, hue=TYPE, data=data_large,  ax=axarr[0], hue_order=hue_order, palette="Set1", width=0.5)

	sns.boxplot(x=X, y=Y, hue=TYPE, data=data_small,  ax=axarr[1], hue_order=hue_order, palette="Set1", width=0.5)
	
	plt.legend(bbox_to_anchor=(1,2.2), loc=2, borderaxespad=0.)
	axarr[0].legend([],[])
	
	axarr[0].set(xlabel='', ylabel='GUIDANCE2 Score')
	axarr[1].set(xlabel='Gene', ylabel='GUIDANCE2 Score')

	axarr[0].set_title("Large dataset", loc="left")
	axarr[1].set_title("Small dataset", loc="left")
	
	set_edge_color(axarr[0])
	set_edge_color(axarr[1])
	
	fig.savefig(output, dpi=300, bbox_inches='tight')	
	
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='')		
	parser.add_argument('-o', required=False,
						default="plot.png",help='output name')	
	args = parser.parse_args()
	
	main(args.o)