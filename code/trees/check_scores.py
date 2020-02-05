from ete3 import Tree #module load python/python-2.7.6
from ete3 import NCBITaxa

tree_path = "/groups/itay_mayrose/nomihadar/trees/rosids_trees/sequences_filtered_zanne/tree_mafft_fabaceae/ExaML_result.fabaceae"

species_in_tree = ['100149', '198858', '198859', '198860', '198863', '198864', '198865', '198866', '198869', '198873', '198874', '198881', '198886', '198899', '198900', '198903', '198904', '198905', '198908', '198910', '198911', '198912', '198914', '200325', '138272', '198892', '539015', '539017', '539019', '539023', '539024', '539025', '539026', '539039', '539040', '539049', '539050', '539051', '539053', '539055', '539056', '539057', '539060', '539063', '539070', '539074', '539078', '539081', '539083', '539088', '539089', '539091', '539100', '539102', '539103', '539105', '539106', '539107', '539108', '539110', '539113', '539114', '539118', '539123', '539126', '539127', '539130', '539137', '539139', '539143', '539147', '539150', '539166', '247895', '379247', '53889', '539071', '539101', '539172', '539173', '539177', '520841', '131024', '131026', '131027']
 

def calc_score2(common_ancestor, species):
	
	score = 0
	
	#traverse the common ancestor's tree in postorder
	for node in common_ancestor.traverse("postorder"):
	
		#if node is a species, check weather it is in the given species list
		if node.is_leaf():
		
			#if species in group, include = 1 and out = 0, o.w the opposite 
			node.add_feature("include", int(node.name in species))
			node.add_feature("out", int(not node.include))
		else:
			
			in_sum = node.children[0].include + node.children[1].include  
			out_sum = node.children[0].out + node.children[1].out
			
			# include: number of children in group, 
			#out: number of children out of group
			node.add_feature("include", in_sum)
			node.add_feature("out", out_sum)
	
	#from the common ancestor's tree get only the monophyly nodes 
	#(those with out == 0)
	monophyly_nodes = common_ancestor.search_nodes(out=0)
	sizes = [node.include for node in monophyly_nodes if not node.is_leaf()]
	if sizes:
		max_monophyly_size = max(sizes)
		score =  max_monophyly_size / float(len(species))
	
	return (score, monophyly_nodes)
	
def calc_score1(common_ancestor, species):
	
	#len of node is number of leaves (species)
	score = float(len(species)) / len(common_ancestor)
	return score

#input tree 
tree = Tree(tree_path, format =1)

common_ancestor = tree.get_common_ancestor(species_in_tree)

print "num species in current group: ", len(species_in_tree)
print "******************************************************"
print "num species in common ancestor: ", len(common_ancestor)

print "score 1: ", len(species_in_tree), "\\" , len(common_ancestor), "= ", calc_score1(common_ancestor, species_in_tree)
print "******************************************************"

(score, monophyly_nodes) = calc_score2(common_ancestor, species_in_tree)

monos = [node for node in monophyly_nodes if not node.is_leaf()]
max_node = monos[0]
max_include = 0
for node in monos:
	if node.include > max_include:
		max_include = node.include
		max_node = node

print "******************************************************"
print "biggest monophyly group: ", len(max_node)
print "score 2: ", len(max_node), "\\" , len(species_in_tree), "= ", score
print "******************************************************"
print max_node

a = [x.name for x in max_node.get_leaves()]
out = tree.get_ascii(show_internal=True)
with open("out", "w") as f:
	f.write(out)
print tree.write(format=1, outfile="new_tree.nw")

a=[x for x in common_ancestor.get_leaves() if x.name in species_in_tree]
print a

