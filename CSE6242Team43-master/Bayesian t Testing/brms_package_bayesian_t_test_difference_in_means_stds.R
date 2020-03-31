library(brms)

df <- read.csv('orig_ALL.txt', sep = '|')[ ,c('DFLT', 'riskPoints')]
df <- df[sample(nrow(df), 20000000), ]

uneq_var_frm <- bf(riskPoints ~ DFLT, sigma ~ DFLT)

mod_uneqvar <- brm(
  uneq_var_frm,
  data = df,
  cores=4
)

summary(mod_uneqvar)
plot(mod_uneqvar)