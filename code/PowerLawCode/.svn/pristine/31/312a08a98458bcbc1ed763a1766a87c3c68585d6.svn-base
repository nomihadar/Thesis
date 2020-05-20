import sys, os

sys.path.append(os.path.dirname(sys.path[0]))

__author__ = 'Dana'

from defs import *
from utils.msa_functions import convert_sequences_ids, get_msa_properties

INNER_DIR = "other_transcriptions"

def main(inputdir, output_path):
	
	d = {}
	for file_name in os.listdir(inputdir):
		family_name = file_name.split(".")[0]
		if family_name in d:
			d[family_name].append(file_name)
		else:
			d[family_name] = [file_name]

	exceptions = []
	for family_name, files_names in d.items():

		family_dir = os.path.join(output_path, family_name)
		os.mkdir(family_dir)

		sizes = []
		for file_name in files_names:
			orig_path = os.path.join(inputdir, file_name)
			(n, length) = get_msa_properties(orig_path)
			sizes.append(n)

		# copy the largest msa (in terms of number of species)
		largest_msa = files_names[np.argmax((sizes))]

		orig_path = os.path.join(inputdir, largest_msa)
		file_fas = os.path.join(family_dir, REF_MSA_FAS)
		file_phy = os.path.join(family_dir, REF_MSA_PHY)

		shutil.copy2(orig_path, file_fas)
		convert_sequences_ids(orig_path, file_phy)

		# copy other transcriptions
		trans_dir = os.path.join(family_dir, INNER_DIR)
		os.mkdir(trans_dir)

		for file_name in files_names:
			if file_name == largest_msa:
				continue

			trans_id = file_name.split(".")[2]  # transcription id
			file_fas = "ref_msa_{0}.aa.fas".format(trans_id)
			file_phy = "ref_msa_{0}.aa.phy".format(trans_id)

			dest_file_fas = os.path.join(trans_dir, file_fas)
			dest_file_phy = os.path.join(trans_dir, file_phy)

			shutil.copy2(orig_path, dest_file_fas)

			try:
				convert_sequences_ids(orig_path, dest_file_phy)
			except:
				exceptions.append(dest_file_fas)
				continue

	d = {"exceptions": exceptions}
	df = pd.DataFrame(d)
	df.to_csv("exceptions.csv")

	d = {"paths": os.listdir(inputdir)}
	df = pd.DataFrame(d)
	df.to_csv("paths.csv")


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='parse selectome files')
	parser.add_argument('--dir_path', '-f', help='directory path with all files')
	parser.add_argument('--destination_path', '-d', help='destination directory path to save the output files')
	args = parser.parse_args()

	inputdir = args.dir_path
	output_path = args.destination_path

	main(inputdir, output_path)

