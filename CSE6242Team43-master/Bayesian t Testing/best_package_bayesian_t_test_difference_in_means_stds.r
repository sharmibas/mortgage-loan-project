
library(BEST)

df <- read.csv('orig_ALL.txt', sep = '|')[ ,c('DFLT', 'riskPoints')]

non_defaults <- subset(df, DFLT==0)$riskPoints
defaults <- subset(df, DFLT==1)$riskPoints

rm(df)

priors <- list(muM = 50, muSD = 50)

BESTout <- BESTmcmc(non_defaults, defaults, priors=priors, parallel=TRUE)

png(filename="/Users/jeffe/Desktop/Bayesian_ttest_CSE6242_project.png")
plotAll(BESTout)
dev.off()

