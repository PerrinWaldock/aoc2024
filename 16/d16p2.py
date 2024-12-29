import numpy as np
from collections import deque
import re
import os
from tqdm import tqdm
import itertools
import sys

import dataclasses
from typing import Any


filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input.txt")
# filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample.txt")
# filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample2.txt")

ROTATE_SCORE = 1000
MOVE_SCORE = 1

lines = deque()
with open(filename) as f:
    for line in f:
        lines.append([c for c in line.strip()])
array = np.array(lines)

start = tuple(np.argwhere(array == "S")[0])
startdir = (0,1)
end = tuple(np.argwhere(array == "E")[0])
enddirs = [(0,1),(0,-1),(1,0),(-1,0)]

def canMoveTo(place):
    return place == "."

def addtuple(a, b):
    return (a[0]+b[0], a[1]+b[1])

def rotateLeft(direction):
    return (-direction[1],direction[0])

def rotateRight(direction):
    return (direction[1],-direction[0])

def getFrontier(position, direction, score):
    return set([(addtuple(position, direction), direction, score + MOVE_SCORE, (position, direction)), (position, rotateLeft(direction), score + ROTATE_SCORE, (position, direction)), (position, rotateRight(direction), score + ROTATE_SCORE, (position, direction))])

def visualize(arr):
    for line in arr:
        print("".join(line))

def explore(position, direction):
    bestscore = dict()
    bestscore[(position,direction)] = (0, set())
    frontier = getFrontier(position, direction, 0)
    while len(frontier) > 0:
        (position, direction, score, previouskey) = frontier.pop()
        if array[*position] == "#":
            continue
        key = (position, direction)
        if not key in bestscore or score < bestscore[key][0]:
            bestscore[key] = (score, set([previouskey]))
            frontier |= getFrontier(position, direction, score)
        elif score == bestscore[key][0]:
            bestscore[key][1].add(previouskey)
    return bestscore

bestscore = explore(start, startdir)

def retrace(endkeys, bestscore):
    traveledNodes = set()
    travelledKeys = set()
    frontier = set(endkeys)
    while len(frontier) > 0:
        key = frontier.pop()
        if key not in bestscore:
            continue
        position = key[0]
        traveledNodes.add(position)
        travelledKeys.add(key)
        possibleNextKeys = bestscore[key][1]
        for k in possibleNextKeys:
            if k not in travelledKeys:
                frontier.add(k)
    return traveledNodes

endscores = []
for enddir in enddirs:
    key = (end, enddir)
    if key in bestscore:
        endscores.append(bestscore[key][0])
lowestscore = min(endscores)
endkeys = [(end, enddir) for enddir in enddirs if bestscore[(end, enddir)][0] == lowestscore]

goodseats = retrace(endkeys, bestscore)
for s in goodseats:
    array[s] = "O"
print(len(goodseats))
            