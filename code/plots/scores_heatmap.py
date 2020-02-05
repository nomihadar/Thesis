from string import ascii_letters
import numpy as np
import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def variance():

	data = pd.read_csv("data.csv")
	df = data.pivot("Ref Tree", "Simulated Tree", "variance")
	fig, ax = plt.subplots()
	mask = np.zeros_like(df)
	mask[np.tril_indices_from(mask)] = True

	sns.heatmap(df,annot=True, fmt=".3f", cmap="YlGnBu")
	fig.savefig("variance.png", dpi=300)
	
def main(output):

	data = pd.read_csv("data.csv")
	df = data.pivot("Ref Tree", "Simulated Tree", "distance")
	

	fig, ax = plt.subplots()

	mask = np.zeros_like(df)
	mask[np.tril_indices_from(mask)] = True

	sns.heatmap(df,annot=True, fmt=".3f", cmap="YlGnBu")
	
	'''
	ax.text(4, 4, "nomiiii", 
			horizontalalignment='center', 
			size='x-small', color='black', weight='semibold')			
	'''
	
	fig.savefig(output, dpi=300)	#, bbox_inches='tight'


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='')		
	parser.add_argument('-o', required=False,
						default="plot.png",help='output name')	
	args = parser.parse_args()
	main(args.o)
	variance()