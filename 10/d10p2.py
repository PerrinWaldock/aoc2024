import numpy as np
from collections import deque
import re
import os
from tqdm import tqdm
import itertools

filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input.txt")
#filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample.txt")
#filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample2.txt")
    

lines = deque()
with open(filename) as f:
	for line in f:
		lines.append([int(c) for c in line.strip()])
array = np.array(lines)

trailheads = np.argwhere(array == 0)
peaks = np.argwhere(array == 0)
connectedPeaks = {tuple(t): 0 for t in trailheads}

def inRange(x, y):
    return 0 <= x < np.shape(array)[0] and 0 <= y < np.shape(array)[1]

def validNextSteps(arr, x, y, step=1):
    height = arr[x,y]
    spotsToTest = [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
    spotsToTest = [(x,y) for (x,y) in spotsToTest if inRange(x,y)]
    return [(x,y) for (x,y) in spotsToTest if arr[x,y] == height+step]

def getConnected(arr, x, y, step=1, end=9):
    if arr[x,y] == end:
        return [(x,y)]
    else:
        nextSteps = validNextSteps(arr, x, y, step=step)
        validNext = []
        for (xn,yn) in nextSteps:
            validNext.extend(getConnected(arr,xn,yn, step=step, end=end))
        return validNext

peakscount = 0
for x,y in trailheads:
    trailheads = getConnected(array,x,y,step=1,end=9)
    peakscount += len(trailheads)
print(peakscount)