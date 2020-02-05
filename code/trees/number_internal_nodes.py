from ete3 import Tree
import sys

t = Tree(sys.argv[1])

i = 0
for node in t.traverse("preorder"):
	if not node.is_leaf():
		node.name = str(i)
		i += 1

print t.get_ascii(show_internal=True)
t.write(format=8, outfile="with_internal_nodes.tree")