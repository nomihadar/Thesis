library(pracma)
library(poweRlaw)
library(MASS)



#options(echo=TRUE) # if you want see commands in output file
args <- commandArgs(trailingOnly = TRUE)
path = args[1]
distr = args[2]
output = args[3]

#y = rnbinom(100, 5, 0.2)
observ = read.table(path)[[1]] #read observations 

if (distr == "negbinom"){
	#This represents the number of failures which occur in a sequence of Bernoulli trials 
	#before a target number of successes is reached. 
	fit = fitdistr(observ, "negative binomial")
	r_estimated = fit$estimate[[1]]
	mu_estimated = fit$estimate[[2]]
	prob_estimated = r_estimated / (r_estimated+mu_estimated)
	r_estimated = ceiling(r_estimated)

	df = data.frame(matrix(NA, nrow = 1, ncol = 2))
	colnames(df) <- c("r","p")
	rownames(df) <- NULL
	df[1, ] = list(r_estimated, prob_estimated)
	write.csv(df, file = output)
}

if (distr == "zipf"){
	zeta_dist = function (k, a) (k^-a / zeta(a))

	fit = fitdistr(observ, zeta_dist, list(a = 1.0001), lower=1.0001, upper=1.99999)
	a_estimated = fit$estimate[[1]]

	df = data.frame(matrix(NA, nrow = 1, ncol = 1))
	colnames(df) <- c("a")
	rownames(df) <- NULL
	df[1, ] = list(a_estimated)
	write.csv(df, file = output)
}

#t = ks.test(y, "pnbinom", r_estimated, prob_estimated)
#df[1, ] = list(r_estimated, prob_estimated, t$p.value)
#df = df[order(df$pvalue, decreasing = TRUE),]
#write.csv(df, file = paste(gene,"_ks_result.csv"))

