import logging
import os 

#input from other file: initialize(__file__)
def initialize(path):

	filename = path
	format = '%(levelname)s, %(asctime)s, %(message)s'
	date_format = '%m/%d/%Y %I:%M:%S'

	logging.basicConfig(filename=filename, format=format, 
						datefmt=date_format, level=logging.INFO)	
						
def initialize2(file_name):

	logfile = os.path.splitext(file_name)[0]  + ".logfile"
	format = '%(message)s'

	logging.basicConfig(filename=logfile, format=format, level=logging.INFO)