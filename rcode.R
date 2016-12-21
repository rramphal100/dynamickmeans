#read file
library(readr)
data <- read_csv("~/data.csv")
View(data)


library(MASS)
ind <- sapply(data, is.numeric)
data[ind] <- lapply(data[ind], scale)

data.features = data
data.features$stock <- NULL 
data.features$date <- NULL



data.weighted = data.features

#add weight then apply k means
data.weighted$percent_change_next_weeks_price <- data.features$percent_change_next_weeks_price*2.0
results <- kmeans( data.weighted , 30)
results
table(data$stock,results$cluster)

library(cluster)
clusplot(data.weighted[12:2], results$cluster, main='2D representation of the Cluster solution',
         color=TRUE, shade=TRUE,
         labels=2, lines=0)

#plot( data[c("percent_change_next_weeks_price","next_weeks_open" )], col = results$cluster )

#dendrogram
table(data$stock,results$cluster)
plot( data[c("percent_change_next_weeks_price" , "next_weeks_open")], col = results$cluster)
clusters <- hclust(dist(data.weighted[, 3:4]))
plot(clusters)


out <- cbind(data.weighted , clusterNum = results$cluster)
head(out)
#pairwise plot
plot(data.weighted, col=results$cluster) 



#elbow method graph
wss <- (nrow(data.weighted)-1)*sum(apply(data.weighted,2,var))
for (i in 2:15) wss[i] <- sum(kmeans(data.weighted,
                                     centers=i)$withinss)
plot(1:15, wss, type="b", xlab="Number of Clusters",
     ylab="Within groups sum of squares")



library(cluster)
clusplot(data.weighted[12:1], results$cluster, main='2D representation of the Cluster solution',
         color=TRUE, shade=TRUE,
         labels=2, lines=0)
