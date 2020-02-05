
R_SIZE = 1000
P_SIZE = 1000

y = rnbinom(100, 5, 0.2)

df = data.frame(matrix(NA, nrow = R_SIZE*P_SIZE, ncol = 3))
colnames(df) <- c("r","p", "pvalue")
rownames(df) <- NULL

p_values = linspace(0.0000001, 1, n = P_SIZE)
i = 0
for (r in 1:R_SIZE) {
  for (p in p_values) {
      t = ks.test(y, "pnbinom", r,p)
      df[i, ] = list(r,p,t$p.value)
      i = i + 1
  }
}
df = df[order(df$pvalue, decreasing = TRUE),]
write.csv(df, file = "negative_binom.csv")

###################################################

A_SIZE = 1000
P_SIZE = 1000

y = rnbinom(100, 5, 0.2)

df = data.frame(matrix(NA, nrow = R_SIZE*P_SIZE, ncol = 3))
colnames(df) <- c("r","p", "pvalue")
rownames(df) <- NULL

a_values = linspace(0.0000001, 1.9999999, n = A_SIZE)
i = 0
for (r in 1:a_values) {
    t = ks.test(y, "pnbinom", r,p)
    df[i, ] = list(r,p,t$p.value)
    i = i + 1

}
df = df[order(df$pvalue, decreasing = TRUE),]
write.csv(df, file = "negative_binom.csv")