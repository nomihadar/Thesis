"""
read lineage table created by the R script and create
an output file of the genus found in this requested rank 
"""
import csv
import sys


RANK = "subfamily"
RANK_VALUE = "Caesalpinioideae"

OUTPUT_FILE = "species in {rank}".format(rank = RANK_VALUE)

if __name__ == "__main__":

	if len(sys.argv) < 2:
		print "please insert arguments"
		sys.exit(0)
		
	#get path of table of lineages
	table_path = sys.argv[1]
	
	#species path
	species_path = sys.argv[2]
	
	#create a list of genus that are found in RANK_VALUE
	with open(table_path, 'r') as csvfile:
		reader = csv.DictReader(csvfile)
		genus_ls = [row["genus"] for row in reader if row[RANK] == RANK_VALUE]
					
	# with open(OUTPUT_FILE, 'w') as outfile:	
		# for genus in genus_ls:
			# outfile.write(genus + "\n")
	
	#
	with open(species_path) as f:
		species_ls = f.readlines()
	
	species_fltered = []
	for species in species_ls:
		genus = species.split("_")[0]
		if genus in genus_ls:
			species_fltered.append(species)
		
	
	