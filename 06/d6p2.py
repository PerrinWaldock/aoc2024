import numpy as np
from collections import deque
import os
from tqdm import tqdm

filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input.txt")
#filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample.txt")

lines = deque()
with open(filename) as f:
	for line in f:
		lines.append(list(line.replace("\n", "")))
arr = np.array(lines)

start = tuple(np.argwhere(arr == "^")[0])
startdir = 0
startposition = (*start, startdir)

def inBounds(x, y, d):
	return 0 <= x < np.shape(arr)[0] and 0 <= y < np.shape(arr)[1]

def causesLoop(testarr):
	currentposition = startposition
	pandd = set()
	pandd.add(currentposition)

	def getNext(x, y, d):
		if d == 0:
			xnew = x-1
			ynew = y
		elif d == 1:
			ynew = y + 1
			xnew = x
		elif d == 2:
			xnew = x+1 
			ynew = y
		elif d == 3:
			ynew = y - 1
			xnew = x
		
		if inBounds(xnew,ynew, d) and testarr[xnew,ynew] == "#":
			d = (d + 1)%4
			return getNext(x,y,d)
		else:
			return xnew,ynew,d

	while inBounds(*currentposition):
		currentposition = getNext(*currentposition)
		if currentposition in pandd:
			return True, pandd
		pandd.add((currentposition))
	return False, pandd

_, positionsToTest = causesLoop(arr)
positionsToTest = list(set([p[0:2] for p in positionsToTest if p != startposition and inBounds(*p)]))

validPositions = deque()
for p in tqdm(positionsToTest):
    newarr = arr.copy()
    newarr[*p] = "#"
    if causesLoop(newarr)[0]:
        validPositions.append(p)
print(len(set(validPositions)))
