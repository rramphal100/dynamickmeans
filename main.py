import numpy as np 
import random as rand
from math import sqrt
from datetime import datetime

def euclideanDistance(list1, list2):
	sum = 0
	for i in range(0, len(list1)):
		sum += (list1[i] - list2[i]) ** 2
	return sqrt(sum)

# Debugging
def printClusSet(set):
	for clus in xrange(0, len(set)):
		print "Cluster #", clus, ": ", set[clus]


# Update centroids based on the average of all the points in that cluster
def updateCentroids(dataSet, centSet, clusSet, k):
	for clus in range(0, k): # For every cluster
		if(len(clusSet[clus]) != 0): # Only update if there are points in the cluster
			newCent = [0.0] * len(dataSet[0])
			for dataRow in clusSet[clus]: # For every point in that cluster
				newCent = [attr1 + attr2 for attr1, attr2 in zip(dataSet[dataRow], newCent)] # Add up all respective points
			centSet[clus] = [attr/len(clusSet[clus]) for attr in newCent]

dataSet = []
centSet = []
clusSet = []
maxValues = []
rand.seed(datetime.now()) # To get different random numbers each time

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

# Start iterations for clustering with dynamic k
for k in range(1, len(dataSet)):
	centSet = []
	clusSet = []
	# Generate random centroid values
	for x in range(0, k):
		randomRow = dataSet[rand.randint(0, len(dataSet)-1)]
		centSet.append(randomRow)
		clusSet.append([])

	# Initialize first set of clusters
	for dataRow in range(0, len(dataSet)): # For every data point
		minDist = 9999999
		assignCluster = 0
		for cent in range(0, k): # For every centroid
			currDist = euclideanDistance(dataSet[dataRow], centSet[cent])
			if(currDist < minDist):
				assignCluster = cent
		clusSet[assignCluster].append(dataRow)

	# Update Centroids
	updateCentroids(dataSet, centSet, clusSet, k)

	# Start assignment process. Stop when all the points belong in the appropriate cluster.
	needsUpdate = True
	while(needsUpdate):
		needsUpdate = False
		for clus in range(0, k): # For every cluster
			for dataRow in clusSet[clus]: # For every data point given a cluster
				# Since all data has been assigned a cluster, just grab the info
				minDist = euclideanDistance(dataSet[dataRow], centSet[clus])
				assignClus = clus
				for cent in range(0, k): # Calculate distance between every centroid
					currDist = euclideanDistance(dataSet[dataRow], centSet[cent])
					if(currDist < minDist):
						assignClus = cent
				if assignClus != clus:
					clusSet[clus].remove(dataRow)
					clusSet[assignClus].append(dataRow)
					needsUpdate = True
		# DON: DELETE THIS AND USE THE LINE BELOW IF YOU WANT CLUSTER AFTER EACH UPDATE
		# WARNING: THERE ARE TOO MANY NUMBERS FOR A HUMAN TO PROCESS
		# VVVVV USE THIS VVVVV
		# printClusSet(clusSet)
		updateCentroids(dataSet, centSet, clusSet, k)

	# Calculate IV
	IV = 0
	for clus in range(0, k):
		for dataRow in clusSet[clus]:
			IV += euclideanDistance(dataSet[dataRow], centSet[clus])

	# Calculate EV
	EV = 0
	for clus1 in range(0, k):
		for dataRow1 in clusSet[clus1]:
			for clus2 in range(clus1+1, k):
				for dataRow2 in clusSet[clus2]:
					EV += euclideanDistance(dataSet[dataRow1], dataSet[dataRow2])
	EV /= len(dataSet)

	if EV != 0:
		print "K = ", k
		printClusSet(clusSet)
		print "IV/EV =", IV/EV
		print "======================================================================="

