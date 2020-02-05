library(ape)
library(geiger)

examined_group = "Fabaceae"

## get all the names of the specified rank within the examined group  
gb_result = gbcontain(examined_group, rank = "genus")
species = gb_result[[1]] 

OUTPUT_FILE = paste("output_all_genera_of", examined_group, sep="_")

#write to output file
write(species, file = OUTPUT_FILE,
      sep = "\n")