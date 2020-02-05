#Testing the power law hypothesis - by the method proposed in CLAUSET 
library(pracma)
library(poweRlaw)
library(MASS)

X_MIN = 1
NUM_SIMULATIONS = 2500
NUM_SIMULATIONS = 1000

#options(echo=TRUE) # if you want see commands in output file
args <- commandArgs(trailingOnly = TRUE)
path = args[1]
output = args[2]

x = read.table(path)[[1]] #read observations 
n = length(x)

#########################################################
# Testing the log-normal hypothesis - package
ln = dislnorm$new(x)
ln$setXmin(X_MIN) #set xmin parameter
est = estimate_pars(ln) 
ln$setPars(est$pars) #set exponent parameter 

ln_bs_p = bootstrap_p(ln, no_of_sims=NUM_SIMULATIONS)
ln_p_value = ln_bs_p$p
#########################################################

#########################################################
 Testing the discrete Poisson hypothesis - package
poi = dispois$new(x)
poi$setXmin(X_MIN) #set xmin parameter
est = estimate_pars(poi) 
poi$setPars(est$pars) #set exponent parameter 

pi_bs_p = bootstrap_p(poi, no_of_sims=NUM_SIMULATIONS)
pi_p_value = pi_bs_p$p
#pi_p_value=-1
#########################################################

#########################################################
#Testing the discrete Exponential hypothesis - package
ex = disexp$new(x)
ex$setXmin(X_MIN) #set xmin parameter
est = estimate_pars(ex) 
ex$setPars(est$pars) #set exponent parameter 

ex_bs_p = bootstrap_p(ex, no_of_sims=NUM_SIMULATIONS)
ex_p_value = ex_bs_p$p
#########################################################


df = data.frame(matrix(NA, nrow = 1, ncol = 3))
colnames(df) <- c("log-normal p_value", "Poisson p_value", "Exponential p_value")
rownames(df) <- NULL
df[1,1] = list(ln_p_value)
df[1,2] = list(pi_p_value)
df[1,3] = list(ex_p_value)
write.csv(df, file = output)


