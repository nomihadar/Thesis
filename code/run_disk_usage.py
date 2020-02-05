import os
import sys
import argparse
from subprocess import call
import run_job

CMD = 'eval echo ~$USER | du -h --max-depth={max_depth} > my_disk_usage.txt'
SH_FILE = "job_disk_usage.sh"

def main(max_depth):
	cmd = CMD.format(max_depth=max_depth)
	run_job.run_job(cmd, SH_FILE)
		
if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='')
	parser.add_argument('--max_depth', '-d', default=1, type = int,
						required=False, help='max depth of directories')
	args = parser.parse_args()

	main(args.max_depth)
	
	