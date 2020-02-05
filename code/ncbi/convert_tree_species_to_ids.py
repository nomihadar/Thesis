import sys
from ete3 import Tree
from ete3 import NCBITaxa
import pandas as pd

['58454', '142615', '77013']

byhand = {'Chamerion latifolium': '33138', 'Escallonia calcottiae': '178793', 
			'Quercus vacciinifolia': '97704', 'Mukdenia rosii': '29766', 
			'Hypochaeris arachnoidea': '312094', 'Pellacalyx saccardians': '61148'}

def main(tree_path):

	ncbi = NCBITaxa()

	tree = Tree(tree_path, format =1)
	
	names = []
	ids = []
	in_magnoliophyta = []
	for leaf in tree:
		name = leaf.name.replace("_", ' ')
		name2taxid = ncbi.get_name_translator([name])
		
		if not name2taxid:
			if name in byhand:
				id = byhand[name]
				magno = "yes"
				
			else:
				id = "not found"
				magno = ""
			
		elif len(name2taxid) > 1:
			id = str(name2taxid[name])
			magno = ""
			print "two ids: ",name
		else:
			id = str(name2taxid[name][0])
			lineage = ncbi.get_lineage(id)
			if 3398 in lineage: #3398 - magnoliophyta id
				magno = "yes"
			else:
				magno = "no"
	
		if id != "not found" and id in ids:
			print "duplicate: ", name, id
			id += "_B"
	
		leaf.name = id
			
		names.append(name)
		ids.append(id)
		in_magnoliophyta.append(magno)
		
	df = pd.DataFrame( {'name': names,'id': ids, 
						'in magnoliophyta': in_magnoliophyta})
	df.to_csv('names_to_ids.csv')
	
	p="/groups/itay_mayrose/nomihadar/trees/magnoliophyta_tree/sequences_filtered_zanne/species/intersect_mytree_zannetree_mangoete3.ls"
	with open(p,'r')as f:
		lines = f.read().splitlines()
	
	species = [x for x in lines if x not in ['58454', '142615', '77013']]
	
	tree.prune(list(set(species)), preserve_branch_length=True)

	tree.write(outfile="tree_ids.tree")

if __name__ == "__main__":

	if len(sys.argv) < 2:
		print "please insert arguments"
		sys.exit(0)
	
	#get path to tree file
	tree_path = sys.argv[1]

	main(tree_path)