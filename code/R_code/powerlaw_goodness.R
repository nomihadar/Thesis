#Testing the power law hypothesis - by the method proposed in CLAUSET 
library(pracma)
library(poweRlaw)
library(MASS)

X_MIN = 1
NUM_SIMULATIONS = 2500
#NUM_SIMULATIONS = 10

zeta_dist = function (k, a) (k^-a / zeta(a))

zeta_cdf_mine = function (k, a) {
  nominator = 0
  for (i in 1:k){
    nominator = nominator + i^-a
  }
  nominator / zeta(a)
}

zeta_cdf = function (k, m_pl) {
  dist_cdf(m_pl, k) #dist_cdf is from the poweRlaw, zeta_cdf_mine(2,alpha1) == zeta_cdf(2,m_pl)
}

#options(echo=TRUE) # if you want see commands in output file
args <- commandArgs(trailingOnly = TRUE)
path = args[1]
output = args[2]

x = read.table(path)[[1]] #read observations 

#estimation of the package
n = length(x)
m_pl = displ$new(x)
m_pl$setXmin(X_MIN) #set xmin parameter
est = estimate_pars(m_pl)
alpha = est$pars 
m_pl$setPars(alpha) #set exponent parameter 


#########################################################
# Testing the power law hypothesis - package
bs_p = bootstrap_p(m_pl, no_of_sims=NUM_SIMULATIONS)
p_value = bs_p$p
#########################################################

#########################################################
# Testing the power law hypothesis - my implementation 
#ks_res = ks.test(x, "zeta_cdf", m_pl) #dist_cdf(m_pl, 2)==zeta_cdf(2, alpha1)
#d0 = as.numeric(ks_res$statistic)

#testresult = numeric(NUM_SIMULATIONS)
#for (i in 1:length(testresult)){
    
#  #generate random from the power law 
#  random = dist_rand(m_pl, n)
  
#  #fit paramaters to the randomal data
#  o_pl = displ$new(random)
#  o_pl$setXmin(X_MIN)
#  est = estimate_pars(o_pl)
#  alpha = est$pars
#  o_pl$setPars(alpha)
  
#  ks_res2 = ks.test(random, "zeta_cdf", o_pl)
#  d = as.numeric(ks_res2$statistic)
#  
#  testresult[i] = as.numeric(d >= d0)
#}
#p_value = sum(testresult) / length(testresult)
#########################################################


df = data.frame(matrix(NA, nrow = 1, ncol = 2))
colnames(df) <- c("alpha", "p_value")
rownames(df) <- NULL
df[1,1] = list(alpha)
df[1,2] = list(p_value)
write.csv(df, file = output)


