import numpy as np
from collections import deque
import re
import os
from tqdm import tqdm
import itertools

filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input.txt")
# #filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample.txt") #140
# filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample2.txt") #1930
    
lines = deque()
with open(filename) as f:
	for line in f:
		lines.append([c for c in line.strip()])
array = np.array(lines)

def inRange(x,y):
	return 0 <= x < np.shape(array)[0] and 0 <= y < np.shape(array)[1]

def inOutsideBorder(x,y):
	p[0] == -1 or p[1] == -1 or p[0] == np.shape(array)[0] or p[1] == np.shape(array)[1]

def getAdjacent(x,y):
	points = [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
	return [p for p in points if inRange(*p)]

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
    print(len(pointsToAllocate) / np.size(array))
    p = pointsToAllocate.pop()
    region = getInRegion(*p)
    allocatedPoints.update(region)
    pointsToAllocate.difference_update(region)
    regions.append(region)

def getArea(region):
    return len(region)
    
# perimeter is sum of number of adjacent squares
def getNonSimilarAdjacentPoints(x,y,value):
    points = [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
    return [p for p in points if p[0] == -1 or p[1] == -1 or p[0] == np.shape(array)[0] or p[1] == np.shape(array)[1] or array[*p] != value]

def getPerimeter(region):
    return np.sum([getNonSimilarAdjacentPoints(p[0], p[1], array[*p]) for p in region])

sum = 0
for region in regions:
    perimeter = getPerimeter(region)
    area = getArea(region)
    sum += perimeter*area
print(sum)