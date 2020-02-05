import csv
import numpy as np


def write_output(groups, group, rank):

	out_file = "scores_{}_{}.csv".format(group, rank)
				
	out_log = "scores_{}_{}.logfile".format(group, rank)
	
	groups_ls = groups.values()
	groups_ls.sort(key = lambda group: group.num_species, reverse=True)
	
	with open(out_file, 'w') as fcsv:
		with open(out_log, 'w') as flog:
		
			csv_writer = csv.writer(fcsv)
			csv_writer.writerow(['group id','num species','score1','score2'])
			
			for group in groups_ls:
				
				flog.write(group.toString() + "\n")
				
				if group.species_intree:

					row = [str(group.taxid), str(group.num_species), 
							group.score1ToStr(), group.score2ToStr()]
					csv_writer.writerow(row)
					
def write_statistic(groups, group, rank):
		
	out_file = "scores_{}_{}_statistics.csv".format(group, rank)
			
	# data = [["minimal # species in group", "# groups", 
				# "score1 average", "score1 median", 
				# "score2 average", "score2 median", "# monophyly"]]
	
	data = [["minimal # species in group", "# groups", 
			"score1 average", "score2 average", "# monophyly"]]
	
	for min_num in [5, 10, 20, 50, 100, 200, 500, 1000]:
		
		#ranks with minimal number of species:
		groups_filtered = [group for group in groups.values() 
							if group.num_species >= min_num]	
		
		if groups_filtered:
			row = stat(groups_filtered, min_num)
			data.append(row)
				
	with open(out_file, "w") as fout:
		fcsv = csv.writer(fout, delimiter=',')
		fcsv.writerows(data)
		
def stat(groups, min_num_species):
			
	#number of monophyly ranks
	num_monophyly = sum([1 for group in groups if group.score1 == 1])
	mono_percent = float(num_monophyly) / len(groups)
	
	#scores1 and their average
	scores1 = [group.score1 for group in groups]
	score1_avg = sum(scores1) / len(scores1)
	score1_median = np.median(scores1) 
	
	#scores2 and their average
	scores2 = [group.score2 for group in groups]
	score2_avg = sum(scores2) / len(scores2)
	score2_median = np.median(scores2) 
	
	row = [min_num_species, len(groups), 
			"{0:.2f}".format(score1_avg),
			#"{0:.2f}".format(score1_median),			
			"{0:.2f}".format(score2_avg),
			#"{0:.2f}".format(score2_median),				
			"{0:.2f}".format(mono_percent)]		
	
	return row