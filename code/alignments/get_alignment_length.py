import os, sys
import numpy as np
from Bio import SeqIO 

sys.path.append("/groups/itay_mayrose/nomihadar/code/")

from alignments import get_foramt as gf

def get_alignment_length(align):
	format = gf.get_foramt(align) 
	records = list(SeqIO.parse(open(align), format))
	return len(records[0].seq)
	
def get_average_seqs_length(align):
	#set average seqs length
	format = gf.get_foramt(align) 
	records = list(SeqIO.parse(open(align), format))
	lengths = [len(record.seq.ungap("-")) for record in records]
	return np.average(lengths)	