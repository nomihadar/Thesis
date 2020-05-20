import sys, os
import fnmatch

__author__ = 'Nomi'

sys.path.append(os.path.dirname(sys.path[0]))

from defs import *

TITLES = [ID_COL, 'replicate', 'SIC', 'SIC_no_edges']




def parse_simple_indel_coding(sic_file, id, replicate="0"):
	if os.path.exists(sic_file):
		df = pd.read_csv(sic_file)

		# numbers of indels
		colname = COL_NAMES_SIC[1]
		num_indels = df[colname].shape[0]
		num_indels_not_inedge = df[df[colname] == False].shape[0]
	else:
		num_indels = "error"
		num_indels_not_inedge = "error"

	data[TITLES[0]].append(id)
	data[TITLES[1]].append(replicate)
	data[TITLES[2]].append(num_indels)
	data[TITLES[3]].append(num_indels_not_inedge)





if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('-f', required=False,
						help='file of paths', default="")
	parser.add_argument('-o', required=False,
						help='output name', default="all_simulations_sic_summary.csv")
	parser.add_argument('-simulations', required=False, action='store_true',
						help='flag')
	args = parser.parse_args()


	data = {name: [] for name in TITLES}
	if not args.f:
		dic = DIC
	else:
		df = pd.read_csv(args.f)
		dic = df.set_index(ID_COL)[PATH_COL].to_dict()


	#for id, rel_path in dic.items():
	for id in [n for n in range(1,101)]:
		rel_path = dic[id]
		if not args.simulations:
			sic_file = os.path.join(DATA_PATH, rel_path, SIC_DIR, SIC_OUTPUT)
			parse_simple_indel_coding(sic_file, id)
		else:
			for i in range(1, N_SIM + 1):
				sic_file = os.path.join(DATA_PATH, rel_path, SIMULATIONS_DIR, SIC_DIR, SIC_DIR_SIM.format(i), SIC_OUTPUT)
				parse_simple_indel_coding(sic_file, id, i)

	df = pd.DataFrame(data)
	df = df[TITLES]
	df.to_csv(args.o, index=False)


