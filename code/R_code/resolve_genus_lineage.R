library(ape)
library(geiger)

# module load R/R310
# R CMD BATCH --no-save --no-restore '--args tree1=file1 tree2=file2' ~/code/resolve_genus_lineage.R tree1 tree2 

OUTPUT_FILE = "output_lineage.csv"

EXAMINED_GROUP = "Streptophyta"
RANK = "family"

# Get arguments 
args <- commandArgs(TRUE)
for(i in 1:length(args)){
 eval(parse(text = args[[i]]))
}

#read input file path 
genus_ls <- scan(input, what="", sep="\n")


final_table <- data.frame()
not_found = 0

#for each species in the input species list
for (genus in genus_ls) {

	#resolve genus 
	table = try(gbresolve(genus, rank=RANK, within = EXAMINED_GROUP))
	
	if (inherits(table,"try-error")){
		print (paste("no resolution for",genus))
		not_found = not_found + 1
		next
	}
	
	if (nrow(final_table)==0)
		final_table <- table
	else
		#merge to one table 
		final_table <- merge(as.data.frame(final_table), 
							as.data.frame(table), all=TRUE)

}

write.table(final_table, file = OUTPUT_FILE, sep = ",", row.names = F)
#species_list = c("Thermopsisfabacea", "Thermopsis rhombifolia", "Piptanthus tomentosus", "Ammopiptanthus mongolicus") 

print (paste("# not found:", not_found))