library(pracma)
library(poweRlaw)
library(MASS)

X_MIN = 1

#options(echo=TRUE) # if you want see commands in output file
args <- commandArgs(trailingOnly = TRUE)
path = args[1]
output = args[2]

#y = rnbinom(100, 5, 0.2)
x = read.table(path)[[1]] #read observations 

#estimation of the package
m_pl = displ$new(x)
n = length(x)
m_pl$setXmin(X_MIN)
est = estimate_pars(m_pl)
alpha1 = est$pars

#fitdist 
zeta_dist = function (k, a) (k^-a / zeta(a))
fit = fitdistr(x, zeta_dist, list(a = 1.0001), lower=1.0001, upper=3)
alpha2 = fit$estimate[[1]]

#etimation of the MLE 
alpha3 = 1 + n*(sum(log(x/(X_MIN-0.5))))^-1
print("nomiiiiiiiiiiiiiiiiiiiiiiiiii")
#write oputput 
df = data.frame(matrix(NA, nrow = 1, ncol = 3))
colnames(df) <- c("alpha1", "alpha2", "alpha3")
rownames(df) <- NULL
df[1,1] = list(alpha1)
df[1,2] = list(alpha2)
df[1,3] = list(alpha3)
write.csv(df, file = output)

print("nomiiiiiiiiiiiiiiiiiiiiiiiiii")



