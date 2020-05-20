import sys, os

sys.path.append(os.path.dirname(sys.path[0]))

__author__ = 'Dana'

import subprocess
from Bio import AlignIO, Alphabet
from defs import *


def get_num_running_jobs():
	#TODO: define user name atomatically
	ps = subprocess.Popen(["qstat", "-u", DANA], stdout=subprocess.PIPE)
	output = subprocess.check_output(["wc", "-l"], stdin=ps.stdout)
	ps.wait()
	num_jobs = int(output.strip())- 5
	return num_jobs #first 5 lines are header


def change_path_permissions_to_777(path):
	os.chmod(path, 0o777)
	for root, dirs, files in os.walk(path):
		for dir in dirs:
			try:
				os.chmod(os.path.join(root, dir), 0o777)
			except:
				pass
		for file in files:
			try:
				os.chmod(os.path.join(root, file), 0o777)
			except:
				pass


def convert_fasta_to_phylip(input_file, output_file):
	with open(input_file, "rU") as input_handle:
		alignments = AlignIO.parse(input_handle, FASTA_FORMAT)
		with open(output_file, "w") as output_handle:
			AlignIO.write(alignments, output_handle, PHYLIP_FORMAT)



def init_commandline_logger(logger):
	logger.setLevel(logging.DEBUG)
	# create console handler and set level to debug
	ch = logging.StreamHandler(sys.stdout)
	ch.setLevel(logging.DEBUG)
	# create formatter
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	# add formatter to ch
	ch.setFormatter(formatter)
	# add ch to logger
	logger.addHandler(ch)


def run_on_paths_list(paths_file):

    df = pd.read_csv(paths_file)
    dirs = df[PATH_COL].tolist()

    for dir in dirs:
        os.chdir(dir)
        if not os.path.exists(SIMULATIONS_DIR):
            os.mkdir(SIMULATIONS_DIR)
        os.chdir(SIMULATIONS_DIR)

        indel_model = os.path.join(dir, SIMULATIONS_DIR, INDEL_MODEL_OUTPUT)
        tree = os.path.join(dir, TREE_RAXML_DIR, TREE_FILE)

        cmd = CMD_PY.format(script=os.path.realpath(__file__),
                            tree=tree,
                            sub_model="WAG",
                            indel_model=indel_model,
                            n=N_SIMULATIONS,
                            output="sim01")

        run_job(cmd, "job_indelible.sh")



if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('-path', required=True,
						help='path to change mode')

	args = parser.parse_args()

	#change_path_permissions_to_777(args.path)
