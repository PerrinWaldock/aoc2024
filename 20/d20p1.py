import numpy as np
from collections import deque
import re
import os
from tqdm import tqdm
import itertools
import sys

import dataclasses
from typing import Any

"""
note: there is only one path through the track. So
1. determine the path through the track (sequence of coordinates)
2. for each point in track, get valid points that are two away
3. find the index of each point that is >= MEANCHEAT from current index

"""

filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input.txt")
# filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample.txt") #44

CHEATDISTANCE = 2
if "sample.txt" in filename:
    MINCHEAT = 1
elif "input.txt" in filename:
    MINCHEAT = 100


lines = deque()
with open(filename) as f:
    for line in f:
        lines.append([c for c in line.strip()])
array = np.array(lines)

start = tuple(np.argwhere(array == "S")[0])
end = tuple(np.argwhere(array == "E")[0])

def canMoveTo(place):
    return place != "#"

def inRange(p):
    return 0 <= p[0] < np.shape(array)[0] and 0 <= p[1] < np.shape(array)[1]

def addtuple(a, b):
    return (a[0]+b[0], a[1]+b[1])

def getAdjacentValidPoints(position, n=1, invalidAllowed=True):
    if n == 1:
        invalidAllowed = False
    adjacentPoints = set([p for p in [addtuple(position, (1,0)), addtuple(position, (0,1)), addtuple(position, (0,-1)), addtuple(position, (-1,0))] if inRange(p) and (invalidAllowed or canMoveTo(array[*p]))])
    if n == 1:
        return adjacentPoints
    else:
        retval = set()
        for ap in adjacentPoints:
            retval |= getAdjacentValidPoints(ap, n=n-1, invalidAllowed=True)
        return retval

def getPath():
    places = deque()
    places.append(start)
    while places[-1] != end:
        avps = getAdjacentValidPoints(places[-1], n=1, invalidAllowed=False)
        for avp in avps:
            if not avp in places:
                places.append(avp)
                continue
    return list(places)

path = getPath()

cheats = deque()
for ind, point in enumerate(path):
    cheatPoints = getAdjacentValidPoints(point, n=CHEATDISTANCE)
    for cp in cheatPoints:
        cpi = path.index(cp)
        if cpi - ind >= MINCHEAT+CHEATDISTANCE:
            cheats.append((point, cp))
print(len(cheats))