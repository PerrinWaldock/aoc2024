import numpy as np
from collections import deque
import os


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

bestscore = {(start, startdir): 0}

def addtuple(a, b):
    return (a[0]+b[0], a[1]+b[1])

def rotateLeft(direction):
    return (-direction[1],direction[0])

def rotateRight(direction):
    return (direction[1],-direction[0])

def getFrontier(position, direction, score):
    return set([(addtuple(position, direction), direction, score + MOVE_SCORE), (position, rotateLeft(direction), score + ROTATE_SCORE), (position, rotateRight(direction), score + ROTATE_SCORE)])

def explore(position, direction):
    bestscore = dict()
    bestscore[(position,direction)] = 0
    frontier = getFrontier(position, direction, 0)
    while len(frontier) > 0:
        (position, direction, score) = frontier.pop()
        if array[*position] == "#":
            continue
        key = (position, direction)
        if not key in bestscore or score < bestscore[key]:
            bestscore[key] = score
            frontier |= getFrontier(position, direction, score)
    return bestscore

bestscore = explore(start, startdir)

endscores = []
for enddir in enddirs:
    key = (end, enddir)
    if key in bestscore:
        endscores.append(bestscore[key])
print(min(endscores))
            