import sys, os, argparse
import numpy as np
import pandas as pd

sys.path.append("/groups/itay_mayrose/nomihadar/code/")

def main():
	
	


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--ranks', '-r', required=True,
						help='number of ranks in tree')
	parser.add_argument('--simulations', '-n', required=True,
						help='number of simulations')			
	args = parser.parse_args()
	

	main(, )