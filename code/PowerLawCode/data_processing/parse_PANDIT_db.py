import sys, os
sys.path.append(os.path.dirname(sys.path[0]))

__author__ = 'Dana'

from defs import *
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio import AlignIO
from Bio.Align import MultipleSeqAlignment


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='parse the PANDIT file')
	parser.add_argument('--db_file', '-f', help='PANDIT file full path')
	parser.add_argument('--destination_path', '-d', help='destination directory path to save the output files')
	args = parser.parse_args()

	db_file = args.db_file
	output_path = args.destination_path

	fam_regex = re.compile("FAM\s+([^\n]*)\n.*?//$", re.DOTALL | re.MULTILINE)
	# NAM\s+((?!DSQ\b)\b\w+)/.*?DSQ\s+([^\n]*)
	alignment_component_regex = re.compile("NAM[ \t]+([^/]*)/[^\n]*\nASQ+[ \t]+([^\n]*)", re.DOTALL | re.MULTILINE)
	# PF00512 is an evil test case
	non_problematic_families = []
	with open(db_file, "r") as db:
		for family_content in fam_regex.finditer(db.read()):
			family_name = family_content.group(1)
			family_dirpath = SEP.join([output_path, family_name])
			seq_records = []
			record_ids_set = set()
			multiples = False
			for alignment_component in alignment_component_regex.finditer(family_content.group(0)):
				sequence_name = alignment_component.group(1)
				sequence_content = alignment_component.group(2).replace(".", "-")
				if not sequence_name in record_ids_set:
					seq_records.append(SeqRecord(Seq(sequence_content), name=sequence_name, id=sequence_name))
					record_ids_set.add(sequence_name)
				else:
					multiples = True
			if not multiples:
				non_problematic_families.append(family_name)
			alignment = MultipleSeqAlignment(seq_records)
			if not os.path.exists(family_dirpath):
				os.mkdir(family_dirpath)
			AlignIO.write([alignment], SEP.join([family_dirpath, REF_MSA_PHY]), PHYLIP_FORMAT)
	#print(non_problematic_families)
