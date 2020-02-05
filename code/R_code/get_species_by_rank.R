library(ape)
library(geiger)


examined_group = "Fabaceae"
myrank = "genus"

OUTPUT_FILE = paste("output", examined_group, "by", myrank, sep="_")

## get all the names of the specified rank within the examined group  
gb_result = gbcontain(examined_group, rank = myrank)
#the result from gbcomtain is a pair where the key is the left argument
taxa = gb_result[[1]] 

#if file exists remove it casue the append flag is on
if (file.exists(OUTPUT_FILE)){
  file.remove(OUTPUT_FILE)
}

iteration = 1

## for each taxa find all species within it 
 for (name in taxa){
    
   print (iteration) 
   
   species = gbcontain(name, rank="species", within=examined_group)
   
   #if there are no specieas print name and continue
   if (is.null(species)) {
     print (paste(name, "was not written to file"))
     next
   }
    
   #create next row
   row = c(name, species[[name]])
   
   #write to output file
   write(row, file = OUTPUT_FILE,
         ncolumns = length(row), 
         append = TRUE, 
         sep = "\t")
   
   iteration = iteration + 1
 
 }

# Warning messages:
#   1: In gbcontain(name, rank = "species", within = examined_group) :
#   Try using the 'within' argument as the following taxa are not unique:
#   Sulla
# 2: In gbcontain(name, rank = "species", within = examined_group) :
#   Try using the 'within' argument as the following taxa are not unique:
#   Pongamia
# 3: In gbcontain(name, rank = "species", within = examined_group) :
#   Try using the 'within' argument as the following taxa are not unique:
#   Bowringia

#species = gbcontain("Bowringia", rank="species", within=examined_group)
