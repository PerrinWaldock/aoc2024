import numpy as np
from collections import deque
import os

filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input.txt")
# filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample.txt") #80
# filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample2.txt") # 1206
# filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample3.txt") #236
# filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample4.txt") #368
# filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample5.txt") #436
	
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

def getArea(region):
	return len(region)

def getValue(region):
	location = region.pop()
	value = array[*location]
	region.add(location)
	return value

def pointsAroundVertex(x,y):
	return [(int(x-.5),int(y-.5)),(int(x+.5),int(y-.5)),(int(x-.5),int(y+.5)),(int(x+.5),int(y+.5))]

def verticesAroundPoint(x,y):
	return [(x-.5,y-.5),(x+.5,y-.5),(x-.5,y+.5),(x+.5,y+.5)]
	
def isEdgeVertex(x,y,region):
	points = pointsAroundVertex(x,y)
	externalOrEdgeSquares = [p for p in points if not inRange(*p) or not p in region]
	return 4 > len(externalOrEdgeSquares) > 0

def getEdgeVerticesInRegion(region):
	edgeVertices = set()
	for (x,y) in region:
		for vx, vy in verticesAroundPoint(x,y):
			if isEdgeVertex(vx,vy,region):
				edgeVertices.add((vx,vy))
	return edgeVertices

def isConnectedEdge(x1,y1,x2,y2,value):
	x,y=((x1+x2)/2,(y1+y2)/2)
	dx,dy=((x2-x1),(y2-y1))
	(xr,yr) = (int(x + dy/2),int(y - dx/2))
	(xl,yl) = (int(x - dy/2),int(y + dx/2))
	leftisvalue = inRange(xl,yl) and array[xl,yl] == value
	rightisvalue = inRange(xr,yr) and array[xr,yr] == value
	return leftisvalue ^ rightisvalue

def countCornerVertex(x, y, value, allVertices):
	points = [(x-1,y),(x,y+1),(x+1,y),(x,y-1)]
	connectedPoints = [p for p in points if p in allVertices and isConnectedEdge(x,y,*p,value)]
	if (len(connectedPoints) == 2 and (np.sqrt((connectedPoints[0][0]-connectedPoints[1][0])**2 + (connectedPoints[0][1]-connectedPoints[1][1])**2) != 2)):
		return 1
	elif len(connectedPoints) == 4:
		return 2
	else:
		return 0

def countSidesInRegion(region):
	edgeVertices = getEdgeVerticesInRegion(region)
	value = getValue(region)
	sides = 0
	for v in edgeVertices:
		newVertices = countCornerVertex(*v,value,edgeVertices)
		sides += newVertices
	return sides
		
pointsToAllocate = set(tuple(p) for p in np.argwhere(array != "."))
regions = deque()
allocatedPoints = set()
while len(pointsToAllocate) > 0:
	p = pointsToAllocate.pop()
	region = getInRegion(*p)
	allocatedPoints.update(region)
	pointsToAllocate.difference_update(region)
	regions.append(region)

sum = 0
for region in regions:
	edgeVertices = getEdgeVerticesInRegion(region)
	sides = countSidesInRegion(region)
	area = getArea(region)
	print(getValue(region), area, sides)
	sum += sides*area
print(sum)