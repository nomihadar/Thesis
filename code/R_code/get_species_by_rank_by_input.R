library(ape)
library(geiger)

# module load R/R310
# R CMD BATCH --no-save --no-restore '--args input=pathtoinput' ~/code/get_species_by_rank_by_input.R temp_for_output

OUTPUT_FILE = "output_lineage_by_family_not_found_only.csv"

EXAMINED_GROUP = "Fabaceae"
RANK = "family"

# Get arguments 
args <- commandArgs(TRUE)
for(i in 1:length(args)){
 eval(parse(text = args[[i]]))
}

#read input file path 
genus_ls <- scan(input, what="", sep="\n")

final_table = data.frame()

not_found = list()

#for each species in the input species list
for (genus in genus_ls) {

	#resolve genus 
	table = try(gbresolve(genus, rank=RANK, within = EXAMINED_GROUP))
	
	if (inherits(table,"try-error")){
		print (paste("no resolution for",genus))
		not_found = c(not_found, genus)
		next
	}
	
	if (nrow(final_table) == 0) {
		final_table <- table
	}
	else {
		#merge to one table 
		final_table <- merge(as.data.frame(final_table), 
							as.data.frame(table), all=TRUE)
	}

}

write.table(final_table, file = OUTPUT_FILE, sep = ",", row.names = F)
#species_list = c("Thermopsisfabacea", "Thermopsis rhombifolia", "Piptanthus tomentosus", "Ammopiptanthus mongolicus") 

print (paste("# not found:", length(not_found)))
print (paste(not_found, sep="\n"))