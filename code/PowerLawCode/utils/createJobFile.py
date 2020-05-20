__author__ = 'Shiran'
import socket


def create_job_file(job_name, command, file_name, error_files_path, job_files_path, python_version="3.5", queue="itaym"):
	hostname = socket.gethostname()
	with open(job_files_path + "/" + file_name, "w") as handle:
		handle.write("#!/bin/tcsh\n\n")  # Vladi said it should be tcsh!
		handle.write("#$ -N " + job_name + "\n")
		handle.write("#$ -S /bin/tcsh\n")
		handle.write("#$ -cwd\n")
		handle.write("#$ -l " + queue + "\n")
		#handle.write("#$ -l h=(compute-7-0)\n")
		#handle.write("#$ -l h=!((compute-7-1))\n")#!((compute-7-1)|(compute-4-29.local)|(compute-8-12)|(compute-8-10))\n")
		# These nodes are not working: (compute-4-47)|(compute-4-24)|(compute-4-46)

		handle.write("#$ -e " + error_files_path + "/$JOB_NAME.$JOB_ID.ER\n")
		handle.write("#$ -o " + error_files_path + "/$JOB_NAME.$JOB_ID.OU\n")
		if python_version == "3.5":
			if hostname == 'jekyl.tau.ac.il' or hostname.startswith("compute-7-") or hostname.startswith("compute-8-") or hostname.startswith("compute-6-"):
				# handle.write("#$ -q comp7.itaym.q,comp8.itaym.q\n")
				handle.write("module load python/anaconda3-5.0.0\n")
			elif hostname == 'lecs2.tau.ac.il' or hostname.startswith("compute-4-"):
				handle.write("module load python/anaconda3-4.0.0\n")
		else:
			if not "anaconda" in python_version:
				handle.write("module load python/python-{0}\n".format(python_version))
			else:
				handle.write("module load python/{0}\n".format(python_version))
		handle.write(command + "\n")
	return job_files_path + "/" + file_name

