import numpy as np
from collections import deque
import os
from tqdm import tqdm


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
coords = list(coords)

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

def corruptMemory(array, coords, n=None):
    memories = deque()
    memories.append(array)
    for ind,coord in enumerate(coords):
        if n is not None and not ind < n:
            break
        memories.append(np.copy(memories[ind]))
        memories[-1][*coord] = "#"
    return memories
        
memories = list(corruptMemory(memory, coords))

for ind, memory in tqdm(enumerate(memories), total=len(memories)):
    bestscore = explore(start, memory)
    if end not in bestscore:
        break
print(ind-1)
print(','.join([str(n) for n in coords[ind-1]]))