import numpy as np
from collections import deque
import re
import os
from tqdm import tqdm
import itertools

"""
todo generate an edge follower that always keeps a certain value on its right
very similar to old, but nextValidVertices must always keep a desired value on the right
"""

# filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input.txt")
# filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample.txt") #80
# filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample2.txt") # 1206
# filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample3.txt") #236
filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample4.txt") #368
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

# pretty sure this is working
def getEdgeVerticesInRegion(region):
	edgeVertices = set()
	for (x,y) in region:
		for vx, vy in verticesAroundPoint(x,y):
			if isEdgeVertex(vx,vy,region):
				edgeVertices.add((vx,vy))
	return edgeVertices

# def isEdge(x1,y1,x2,y2):
# 	x,y=((x1+x2)/2,(y1+y2)/2)
# 	dx,dy=((x2-x1),(y2-y1)) #whichever one == 0, want the opposite for squares
# 	# print(x1,y1,x2,y2,x,y)
# 	if dy != 0:
# 		xa = int(x+.5)
# 		xb = int(x-.5)
# 		ya = int(y)
# 		yb = int(y)
# 	elif dx != 0:
# 		ya = int(y+.5)
# 		yb = int(y-.5)
# 		xa = int(x)
# 		xb = int(x)
# 	else:
# 		return False
# 	return not inRange(xa,ya) or not inRange(xb,yb) or array[xa,ya] != array[xb,yb]

def getSquaresBetweenVertices(x1,y1,x2,y2):
	x,y=((x1+x2)/2,(y1+y2)/2)
	dx,dy=((x2-x1),(y2-y1))
	if dy != 0:
		xa = int(x+.5)
		xb = int(x-.5)
		ya = int(y)
		yb = int(y)
	elif dx != 0:
		ya = int(y+.5)
		yb = int(y-.5)
		xa = int(x)
		xb = int(x)
	return [p for p in [(xa,ya),(xb,yb)] if inRange(*p)]

def isConnectedEdge(x1,y1,x2,y2,value):
	x,y=((x1+x2)/2,(y1+y2)/2)
	dx,dy=((x2-x1),(y2-y1))
	(xr,yr) = (int(x + dy/2),int(y - dx/2))
	(xl,yl) = (int(x - dy/2),int(y + dx/2))
	return inRange(xr,yr) and array[xr,yr] == value and not (inRange(xl,yl) and array[xl,yl] == value) #TODO and getSquaresBetweenVertices different

def nextValidVertices(x,y,value,allVertices,invalid):
	points = [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
	points = [p for p in points if not p in invalid and p in allVertices and isConnectedEdge(x,y,*p,value)]
	return points

def pickValidVertex(x,y,dx,dy,vertices):
    #pick left, then center, then right
    possiblePoints = [(x+dy,y-dx),(x+dx,y+dy),(x-dy,y+dx)]#[(x-dy,y+dx),(x+dx,y+dy),(x+dy,y-dx)]
    for pp in possiblePoints:
        if pp in vertices:
            return pp


# def nextValidVerticesOrdered(p,d,value,allVertices,invalid):
# 	# valid directions: left, forward, right. Preference goes left, forward, right. Ordered by increasing preference
# 	if d != (0,0):
# 		possiblePoints = [(p[0] + d[1], p[1] - d[0]), (p[0] + d[0], p[1] + d[1]), (p[0] - d[1], p[1] + d[1])]
# 	else:
# 		possiblePoints = nextValidVertices(*p,value,allVertices,invalid)
# 	print("pp", p, d, possiblePoints)
# 	return [pp for pp in possiblePoints if not pp in invalid and pp in allVertices and isConnectedEdge(*pp,*p,value)]

def getCornerVertex(edgeVertices):
	return min(list(edgeVertices), key=lambda x: -x[0]-x[1]) #TODO algorithm should be agnostic to key provided it picks any corner

#this loops clockwise from bottom right corner (xmax,ymax)
#TODO try tracking position AND direction as a way to deal with mobius points
#should also help with the starting point problem
def countSidesInRegion(region):
	edgeVertices = getEdgeVerticesInRegion(region)
	value = getValue(region)
	traversed = set()
	direction = (0,0)
	sides = 0
	(x,y) = getCornerVertex(edgeVertices) #need to start in a corner or the algorithm won't work
	startPoint = (x,y)
	iteration = 0
	while len(edgeVertices) > 0:
		validNextSteps = nextValidVertices(x,y,value,edgeVertices,traversed)#nextValidVerticesOrdered((x,y),direction,value,edgeVertices,traversed) 
		print(validNextSteps)
		if startPoint in validNextSteps and len(validNextSteps) > 1:
			print("skipped!")
			validNextSteps.remove(startPoint)

		mobiusPoint = False
		if len(validNextSteps) > 1:
			mobiusPoint = True
			validNextSteps = [pickValidVertex(x,y,direction[0],direction[1],validNextSteps)]
   
		print((x,y), sides, validNextSteps, len(traversed), len(edgeVertices), end="\n\n")
   
		if len(validNextSteps) > 0:
			(xn,yn) = validNextSteps.pop()
			edgeVertices.remove((xn,yn))
			if mobiusPoint: #add if mobius strip point
				edgeVertices.add((xn,yn))
			newdirection = (xn-x,yn-y)
			if newdirection != direction:
				sides += 1
			direction = newdirection
		else: #
			(xn,yn) = getCornerVertex(edgeVertices)
			direction = (0,0)
			startPoint = (xn,yn)
		if (x,y) == (xn,yn):
			# sides -= 1
			print("breaking out because stuck")
			break
		(x,y) = (xn,yn)
		if not mobiusPoint:
			traversed.add((x,y)) #only add new point
  
		iteration += 1
		#if iteration > 50:
		#	break
	return sides

# want A: 4 B 4 C 8 D 4 E 4	

# if "sample2.txt" in filename:
# 	order = [c for c in "RICFVJCEIMS"]
# 	def orderer(r):
# 		r = list(r)
# 		value = array[*r[0]]
# 		return order.index(value)
# 	regions = sorted(regions, key=orderer)

		
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
	# if getValue(region) != "M":
	# 	continue
	edgeVertices = getEdgeVerticesInRegion(region)
	sides = countSidesInRegion(region)
	area = getArea(region)
	print(getValue(region), area, sides)
	sum += sides*area
print(sum)

# 891681 is too low
# 890296 also too low (using top left corner)
# 893451 too low (using bottom right corner)
# 541592 too low