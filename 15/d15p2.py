import numpy as np
from collections import deque
import os
from tqdm import tqdm

filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input.txt")
# filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample.txt")
# filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample2.txt")
# filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample3.txt")

warehouse = deque()
directions = deque()
processingWarehouse = True
with open(filename) as f:
    for line in f:
        line = line.strip()
        if line == "":
            processingWarehouse = False
            continue
        if processingWarehouse:
            newline = deque()
            for c in line:
                if c == "#":
                    newline.extend(['#', '#'])
                elif c == "O":
                    newline.extend(['[', ']'])
                elif c == ".":
                    newline.extend(['.','.'])
                elif c == "@":
                    newline.extend(['@','.'])
            warehouse.append(newline)
        else:
            directions.extend([c for c in line])

dLookup = {'^': (-1,0), 'v': (1,0), '>': (0,1), '<': (0,-1)}

directions = list(directions)
warehouse = np.array(warehouse)
robot = np.argwhere(warehouse == "@")[0]

def visualize(arr):
    for line in arr:
        print("".join(line))

def swap(arr, a, b):
    temp = arr[*a]
    arr[*a] = arr[*b]
    arr[*b] = temp

#TODO easiest to explore then push all at once. break into two chunks?
    #explore: if valid to move, return a list of points that should be moved. Otherwise, return None?
    #push: shift all points one in that direction

def pointsToPush(position, direction):
    nextposition = position + direction #TODO this should be an array. Iterate through.
    nextpositions = [nextposition]
    if direction[0] != 0: #vertical
        if warehouse[*nextposition] == "[":
            nextpositions.append(nextposition + (0,1))
        elif warehouse[*nextposition] == "]":
            nextpositions.append(nextposition + (0,-1))
    
    pointsToMove = list()
    for nextposition in nextpositions:
        if warehouse[*nextposition] == "#":
            return None
        elif warehouse[*nextposition] == ".":
            pointsToMove.append(position)
        elif warehouse[*nextposition] in "[]":
            toAdd = pointsToPush(nextposition, direction)
            if toAdd is None:
                return None
            else:
                pointsToMove.extend(toAdd)
    pointsToMove.append(position)
    return pointsToMove

def pushPoints(points, direction):
    if points is None:
        return
    
    points = set([tuple(p) for p in points])
    
    if direction == (-1, 0): #TODO these could be wrong
        def sortMetric(p):
            return p[0]
    elif direction == (1, 0):
        def sortMetric(p):
            return -p[0]
    elif direction == (0, 1):
        def sortMetric(p):
            return -p[1]
    elif direction == (0, -1):
        def sortMetric(p):
            return p[1]
    
    points = sorted(list(points), key=sortMetric)
    
    for point in points:
        swap(warehouse, point, np.array(point)+direction)
            

def calcGps(position):
    return 100*position[0]+position[1]

def calcAllGps(warehouse):
    boxes = np.argwhere(warehouse == "[")
    sum = 0
    for box in boxes:
        sum += calcGps(box)
    return sum

visualize(warehouse)
for direction in tqdm(directions):
    dir = dLookup[direction]
    robot = np.argwhere(warehouse == "@")[0] #TODO could be made more efficient
    points2push = pointsToPush(robot, dir)
    pushPoints(points2push, dir)
    # visualize(warehouse)
print(calcAllGps(warehouse))
