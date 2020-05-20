#module load R/3.5.1    # -> in jekyl, don't know if exists in power
#R CMD BATCH --no-save --no-restore '--args sic_output.csv test_result.csv' powerlaw_goodness.R output_of_R.txt

#Testing the power law hypothesis - by the method proposed in CLAUSET 
library(MASS)
library(poweRlaw)


X_MIN = 1
NUM_SIMULATIONS = 2500

#options(echo=TRUE) # if you want see commands in output file
args <- commandArgs(trailingOnly = TRUE)
path = args[1] #path to observations file
output = args[2]

#read observations 
col_indel_length = "length"
x = read.csv(path)[[col_indel_length]]

#estimation of the package
n = length(x) #get number of observations
m_pl = displ$new(x) #discrete power-law
m_pl$setXmin(X_MIN) #set xmin parameter
est = estimate_pars(m_pl) #estimate alpha (exponent) parameter
alpha = est$pars #get alpha parameter
m_pl$setPars(alpha) #set alpha parameter 

#########################################################
# Testing the power law hypothesis - package
bs_p = bootstrap_p(m_pl, no_of_sims=NUM_SIMULATIONS)
p_value = bs_p$p #get p-value of test
#########################################################

#write output in the discussing syntax of R
df = data.frame(matrix(NA, nrow = 1, ncol = 2))
colnames(df) <- c("alpha", "p_value")
rownames(df) <- NULL
df[1,1] = list(alpha)
df[1,2] = list(p_value)
write.csv(df, file = output)


