library(ape)

# module load R/R310
# R CMD BATCH --no-save --no-restore '--args tree1=' ~/code/treedist.R temp_for_output

args <- commandArgs(TRUE)

t1=read.tree(file = args[1])
t2=read.tree(file = args[2])
print(args[1])
d = dist.topo(t1,t2,method="score")

print(d)
write(d, file = "temp_treedist_R")

