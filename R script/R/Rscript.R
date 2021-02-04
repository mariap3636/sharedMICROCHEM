
library(igraph)
library(dplyr)
library(data.table)

cmps <- data.frame(fread("ResultFileForR.csv", drop=c(4,5,6), sep="\t", nrows=100, header=TRUE))

cmps2 <- data.frame(fread("ResultFileForR.csv", drop=c(1,2,3), sep="\t", nrows=100, header=TRUE))

cmps = union(cmps,cmps2)

relations <- data.frame(from=c(fread("ResultFileForR.csv", 
	select=c(1), sep="\t", nrows=100)),to=c(fread("ResultFileForR.csv", select=c(4), sep="\t",nrows=100)))

g <- graph_from_data_frame(relations, directed=FALSE,vertices=cmps)

V(g)$color <- ifelse(V(g)$eawag=="1","blue", ifelse(V(g)$alam=="1","red","white")) 
test.layout <- layout_(g,with_dh(weight.edge.lengths = edge_density(g)/10000000))
plot(g, layout=test.layout, vertex.label.color="black")


