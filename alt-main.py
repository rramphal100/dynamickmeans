from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets

dataSet = []
stockSet = []
maxValues = []


# Read data input, get the max values to normalize
with open("dow_jones_index.data", "r") as file:
	columns = len(file.readline().split(",")) # Ignore first row
	maxValues = [0] * columns
	for line in file:
		lineList = line.split(",")[3:-1]
		lineList.append(line.split(",")[-1][:-2]) # Last column has trailing \r\n
		if '' not in lineList:
			lineList = [abs(float(attr)) for attr in lineList] # Convert everything to positive float
			maxValues = [max(maxVal, dataVal) for maxVal, dataVal in zip(maxValues, lineList)]

# Read data input, initialize data set
with open("dow_jones_index.data", "r") as file:
	file.readline() # Ignore first row
	for line in file:
		lineList = line.split(",")[3:-1]
		lineList.append(line.split(",")[-1][:-2]) # Last column has trailing \r\n
		if '' not in lineList: # Ignore data row with missing values
			lineList = [float(i) for i in lineList] # Convert strings to float
			lineList = [dataVal / maxVal for dataVal, maxVal in zip(lineList, maxValues)] # Normalize by dividing by max value
			dataSet.append(lineList)

with open("dow_jones_index.data", "r") as file:
	file.readline() # Ignore first row
	counter = 0
	for line in file:
		stockName = line.split(",")[1]
		if '' not in lineList:
			stockSet.append(stockName)
			counter += 1

dataArray = np.array(dataSet)
kmeans = KMeans(n_clusters=4, random_state=0).fit(dataArray)

# This will print the cluster number that each data point from dataSet list belongs to
print kmeans.labels_

for i in range(len(kmeans.labels_)):
	print stockSet[i], ": ", kmeans.labels_[i]

print kmeans.cluster_centers_

for i in range(len(dataSet[0])):
	avg = 0
	for j in range(len(dataSet)):
		avg = avg + dataSet[j][i]
	print avg / len(dataSet), ", ",

print '\n'
