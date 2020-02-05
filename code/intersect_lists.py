import sys
import os
from subprocess import call
from ete3 import Tree


def intersect(list1_path, list2_path):
	
	with open (list1_path, 'r') as f:
		list1 = f.read().splitlines() 
	
	with open (list2_path, 'r') as f:
		list2 = f.read().splitlines()
	print "length of first list: ", len(list1)
	print "length of second list: ", len(list2)
	intersection = set(list1).intersection(list2)
	
	print "length of intersection: ", len(intersection)
	
	ls = [x for x in list1 if x not in list2]
	print "length of not in intersection: ", len(ls)
	
	return intersection
	
def write_output(intersection, output_name):
	
	with open (output_name, 'w') as f:
		f.write('\n'.join(intersection))
	
if __name__ == "__main__":

	if len(sys.argv) < 4:
		print "please insert arguments"
		sys.exit(0)
	
	list1_path = sys.argv[1]
	
	list2_path = sys.argv[2]
	
	output_name = sys.argv[3]
	
	intersection = intersect(list1_path, list2_path)
	
	#write_output(intersection, output_name)
	
	
	