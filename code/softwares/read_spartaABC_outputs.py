import numpy as np
import sys
import os

sys.path.append("/groups/itay_mayrose/nomihadar/code/")

OUTPUT = "spartaABC_final_indel_param.csv"
NUM_ROWS = 50

def read_output(output_path):
	
	#parameters values of 
	values = np.genfromtxt(output_path, delimiter = '\t', skip_header = 2)
	return values[:, 0:4]
		
def write_output(values, sparta_path):

	#sort by distances (sort from min to max)
	#values.sort(axis = 0)
	distances = values[:,0]
	values = values[distances.argsort()]
	
	header = ('DISTANCE', 'RL', 'A', 'IR')
	header2 = ('rl', 'a', 'ir')
	
	#save output 
	np.savetxt(sparta_path, values, delimiter="\t", fmt = "%.5f", 
				header = "\t".join(header), comments = '') 
	
	#save the mean of the best NUM_ROWS rows
	best = values[:NUM_ROWS, 1:]
	means = np.mean(best, axis=0)
	np.savetxt(OUTPUT, means.reshape(1, means.shape[0]), 
				delimiter=",", fmt = "%.6f", 
				header = ",".join(header2), comments = '') 
	'''
	columns = ['distance', 'rl', 'ir', 'a']
	data = [[int(rl), float(ir), float(a)]]
	df = pd.DataFrame(data, columns=columns, index=[file_name])			
	df.to_csv(OUTPUT)
	'''
def main(outputs_path, gene):
		
	paths = []
	sparta_path = "spartaABC_output.txt" #sparta_path = "spartaABC_output.txt".format(gene = gene)
	for subdir, dirs, files in os.walk(outputs_path):
		for file in files:
			filepath = subdir + os.sep + file
			if gene in subdir and filepath.endswith(sparta_path):
				paths.append(filepath)
	
	concatenated = np.empty((0,4))
	for path in paths:
		
		try:
			values = read_output(path)
		except:
			continue
			
		concatenated = np.concatenate((concatenated, values), axis=0)
	
	print "num iterations: ", len(concatenated)
	
	#write output
	write_output(concatenated, sparta_path)

if __name__ == "__main__":

	if len(sys.argv) < 2:
		print "please insert arguments"
		sys.exit(0)
	
	gene = sys.argv[1]
	
	#direcroty contains sparat outputs 
	outputs_path = sys.argv[2]
	
	main(outputs_path, gene)
	
	