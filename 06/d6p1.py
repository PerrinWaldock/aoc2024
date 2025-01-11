import numpy as np
from collections import deque
import os

filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input.txt")
#filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample.txt")

lines = deque()
with open(filename) as f:
    for line in f:
        lines.append(list(line.replace("\n", "")))
arr = np.array(lines)

directions = deque()
positions = deque()
start = tuple(np.argwhere(arr == "^")[0])
positions.append(start)
directions.append(0)

def inBounds(x, y):
    return 0 <= x < np.shape(arr)[0] and 0 <= y <= np.shape(arr)[1]

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
    
    if inBounds(xnew,ynew) and arr[xnew,ynew] == "#":
        d = (d + 1)%4
        return getNext(x,y,d)
    else:
        return xnew,ynew,d

while inBounds(*positions[-1]):
    x,y,d = getNext(*positions[-1],directions[-1])
    positions.append((x,y))
    directions.append(d)

landedPositions = list(set(positions))
print(len(landedPositions) - 1)