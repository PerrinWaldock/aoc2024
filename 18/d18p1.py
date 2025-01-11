import numpy as np
from collections import deque
import os


filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input.txt")
# filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample.txt")

if "sample.txt" in filename:
    GRIDSIZE = 7
    NANOSECONDS = 12
elif "input.txt" in filename:
    GRIDSIZE = 71
    NANOSECONDS = 1024

coords = deque()
with open(filename) as f:
    for line in f:
        coords.append([int(c.strip()) for c in line.split(",")])

start = (0,0)
end = (GRIDSIZE-1,GRIDSIZE-1)

memory = np.array([['.' for __ in range(GRIDSIZE)] for _ in range(GRIDSIZE)])

def canMoveTo(place):
    return place == "."

def inRange(p):
	return 0 <= p[0] < GRIDSIZE and 0 <= p[1] < GRIDSIZE

def addtuple(a, b):
    return (a[0]+b[0], a[1]+b[1])

def getFrontier(position, score, array):
    return set([(p,score+1) for p in [addtuple(position, (1,0)), addtuple(position, (0,1)), addtuple(position, (0,-1)), addtuple(position, (-1,0))] 
            if inRange(p) and canMoveTo(array[*p])])

def visualize(arr):
    for line in arr:
        print("".join(line))

def explore(position, array):
    steps = dict()
    steps[position] = 0
    frontier = getFrontier(position, 0, array)
    while len(frontier) > 0:
        position, score = frontier.pop()
        if array[*position] == "#":
            continue
        key = position
        if not key in steps or score < steps[key]:
            steps[key] = score
            frontier |= getFrontier(position, score, array)
    return steps

def corruptMemory(array, n=10000):
    memories = dict()
    memories[0] = array
    for ind,coord in enumerate(coords):
        if not ind < n:
            break
        memories[ind+1] = np.copy(memories[ind])
        memories[ind+1][*coord] = "#"
    return memories
        
memories = corruptMemory(memory, NANOSECONDS)
memory = memories[NANOSECONDS]
visualize(memory)

bestscore = explore(start, memory)
print(bestscore[end])