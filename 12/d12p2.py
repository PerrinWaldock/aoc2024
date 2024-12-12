import numpy as np
from collections import deque
import re
import os
from tqdm import tqdm
import itertools

# filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input.txt")
filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample.txt") #140
# filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample2.txt") #1930
	
lines = deque()
with open(filename) as f:
	for line in f:
		lines.append([c for c in line.strip()])
array = np.array(lines)

# identify regions
# find area and perimeter of regions
# multiply together for each region
# sum

def getAdjacent(x,y):
	points = [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
	return [p for p in points if 0 <= p[0] < np.shape(array)[0] and 0 <= p[1] < np.shape(array)[1]]

def getNextPoints(x,y,value,region):
	return [p for p in getAdjacent(x,y) if array[p[0],p[1]] == value and p not in region]

def getInRegion(x, y):
	region = set()
	value = array[x,y]
	region.add((x,y))
	adjacentValid = deque()
	adjacentValid.append((x,y))
	while len(adjacentValid) > 0:
		region.update(adjacentValid)
		adjacentValid.extend(getNextPoints(*(adjacentValid.pop()), value, region))
	return region
		
pointsToAllocate = set(tuple(p) for p in np.argwhere(array != "."))
regions = deque()
allocatedPoints = set()
while len(pointsToAllocate) > 0:
	p = pointsToAllocate.pop()
	region = getInRegion(*p)
	allocatedPoints.update(region)
	pointsToAllocate.difference_update(region)
	regions.append(region)

def getNonSimilarAdjacentPoints(x,y,value):
	points = [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
	return [p for p in points if p[0] == -1 or p[1] == -1 or p[0] == np.shape(array)[0] or p[1] == np.shape(array)[1] or array[*p] != value]

def getBorderingLocations(region):
	return set([ap for p in region for ap in getNonSimilarAdjacentPoints(p[0], p[1], array[*p])])

def getArea(region):
	return len(region)

def getAdjacentPointsIn(x,y,region):
	points = [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
	return [p for p in points if p in region]

def getNumberOfSides(border):
	pointsToAllocate = border.copy() #TODO border doesn't include diagonals
	allocatedPoints = set()
	(x,y) = pointsToAllocate.pop()
	adjacent = getAdjacentPointsIn(x,y,pointsToAllocate)
	direction = (0,0)
	sides = 0
	while len(pointsToAllocate) > 0:
		if len(adjacent) > 0:
			newdirection = (adjacent[0][0] - x, adjacent[0][0] - y)
			(x,y) = adjacent[0]
			pointsToAllocate.remove((x,y))
			if newdirection != direction:
				sides += 1
			direction = newdirection
		else:
			(x,y) = pointsToAllocate.pop()
			direction = (0,0)
		adjacent = getAdjacentPointsIn(x,y,pointsToAllocate)
	return sides


sum = 0
for region in regions:
	border = getBorderingLocations(region)
	sides = getNumberOfSides(border)
	area = getArea(region)
	print(array[*region.pop()], area, sides, border)
	sum += sides*area
print(sum)