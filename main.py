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
def printSet(set):
	for line in set:
		print(line)

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
rand.seed(datetime.now()) # To get different random numbers each time

with open("dow_jones_index.data", "r") as file:
	file.readline(); # Ignore first row
	for line in file:
		lineList = line.split(",")[3:-1]
		lineList.append(line.split(",")[-1][:-2]) # Last column has trailing \r\n
		if '' not in lineList: # Ignore data row with missing values
			lineList = [float(i) for i in lineList] # Convert strings to float
			dataSet.append(lineList)

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
		print IV/EV
		print "========================"

