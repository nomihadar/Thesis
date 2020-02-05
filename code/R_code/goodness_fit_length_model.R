library(pracma)
library(poweRlaw)

options(echo=TRUE) # if you want see commands in output file
args <- commandArgs(trailingOnly = TRUE)
path = args[1]

# R_SIZE = 1000

# #y = rnbinom(100, 5, 0.2)
# y = read.table(path)[[1]]

# p_values = seq(from = 0.001, to = 1, by=0.001)
# p_size = length(p_values)

# df = data.frame(matrix(NA, nrow = R_SIZE*p_values, ncol = 3))
# colnames(df) <- c("r","p", "pvalue")
# rownames(df) <- NULL

# i = 0
# for (r in 1:R_SIZE) {
  # for (p in p_values) {
      # t = ks.test(y, "pnbinom", r,p)
      # df[i, ] = list(r,p,t$p.value)
      # i = i + 1
  # }
# }
# df = df[order(df$pvalue, decreasing = TRUE),]
# write.csv(df, file = "negative_binom.csv")


# path = args[1]
# #y = rnbinom(100, 5, 0.2)
# y = read.table(path)[[1]]

# #estimate paramaeters with negative binomial 
# fitdistr(y, "negative binomial")

# df = data.frame(matrix(NA, nrow = 1, ncol = 3))
# colnames(df) <- c("r","p", "pvalue")
# rownames(df) <- NULL

# t = ks.test(y, "pnbinom", r,p)
# df[1, ] = list(r,p,t$p.value)

# df = df[order(df$pvalue, decreasing = TRUE),]
# write.csv(df, file = "negative_binom.csv")

###################################################

finite_power_low = function (num_vals, a_shape_param)
{
  zeta_of_a = zeta(a_shape_param)
  probs = rep(0,num_vals)
  
  for (i in 1:num_vals)
  {
    probs[i] = i^(-a_shape_param) / zeta_of_a
  }
  
  probs[num_vals] = probs[num_vals] + (1 - sum(probs))
  
  return (probs)
}


#y = rnbinom(100, 5, 0.2)
y = read.table(path)[[1]]

 = fitdistr(y, "negative binomial")

df = data.frame(matrix(NA, nrow = 1, ncol = 2))
colnames(df) <- c("a","pvalue")
rownames(df) <- NULL

t = ks.test(y, "", a)
df[1, ] = list(a,t$p.value)

df = df[order(df$pvalue, decreasing = TRUE),]
write.csv(df, file = paste(gene,"_ks_result.csv"))

r_estimated = t[1]$estimate[[1]]
mu_estimated = t[1]$estimate[[2]]

prob = r_estimated / (r_estimated+mu_estimated)

