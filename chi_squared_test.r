#install.packages("jsonlite")
#install.packages("mosaic")

library(jsonlite)
library(mosaic)

df <- fromJSON("experiment_sample_data.json")

tally(~city+mention, data=df, margins=T)

mentiontable <- tally(~city+mention, data=df)

mentiontable

chisq.test(mentiontable)$expected

tally(~mention, data=df)

chisq.test(mentiontable)$expected

mosaicplot(mentiontable, shade=T)
