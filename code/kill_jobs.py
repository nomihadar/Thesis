import os
import sys

def kill_jobs(start, end):
	for i in range(start, end):
		os.system("qdel " + str(i))
		
if __name__ == "__main__":

	if len(sys.argv) < 3:
		print "please insert arguments"
		sys.exit(0)
		
	start = int(sys.argv[1])
	end = int(sys.argv[2])
	
	kill_jobs(start, end)