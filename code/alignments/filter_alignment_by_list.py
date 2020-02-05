import sys

def filter_sequences_by_list(msa_path, taxa_path):

	with open(msa_path, 'r') as fin:
		msa = fin.read().splitlines()
		
	with open(taxa_path, 'r') as fin:
		taxa_ls = fin.read().splitlines()

	temp=[]
	new_msa = []
	for i, line in enumerate(msa):
		
		if ">" in line:
			taxid = line.replace(">","").strip()
			temp.append(taxid)
			if taxid in taxa_ls:
				
				new_msa.append(msa[i])
				new_msa.append(msa[i+1])
			
	print "# species before filtering: ", len(msa)/2				
	print "# species after filtering: ", len(new_msa)/2		
	
	return new_msa
	
def write_output(new_msa, output_name):	
	
	with open(output_name, 'w') as outf:
		
		for item in new_msa:
			outf.write(item + "\n")
	
	
if __name__ == "__main__":

	if len(sys.argv) < 4:
		print "please insert arguments"
		sys.exit(0)
		
	#get path of fasta file
	msa_path = sys.argv[1]
	
	#species path
	taxa_path = sys.argv[2]
	
	output_name = sys.argv[3]
	
	new_msa = filter(msa_path, taxa_path)

	write_output(new_msa, output_name)

					

	
	