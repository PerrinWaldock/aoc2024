import numpy as np
from collections import deque
import os
from tqdm import tqdm

filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input.txt")
#filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample.txt")
#filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample2.txt")

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
            warehouse.append([c for c in line])
        else:
            directions.extend([c for c in line])

dLookup = {'^': (-1,0), 'v': (1,0), '>': (0,1), '<': (0,-1)}

directions = list(directions)
warehouse = np.array(warehouse)
robot = np.argwhere(warehouse == "@")[0]
print(warehouse)
print(directions)
print(robot)

def swap(arr, a, b):
    temp = arr[*a]
    arr[*a] = arr[*b]
    arr[*b] = temp

def push(position, direction):
    #recursively call to push. return true if success, false if not. Only move if above boxes also moved
    #TODO could be made more efficient by only moving to the . space
    nextposition = position + direction
    if warehouse[*nextposition] == "#":
        return False
    elif warehouse[*nextposition] == ".":
        swap(warehouse, position, nextposition)
        return True
    elif warehouse[*nextposition] == "O":
        canPush = push(nextposition, direction)
        if canPush:
            swap(warehouse, position, nextposition)
        return canPush

def calcGps(position):
    return 100*position[0]+position[1]

def calcAllGps(warehouse):
    boxes = np.argwhere(warehouse == "O")
    sum = 0
    for box in boxes:
        sum += calcGps(box)
    return sum

for direction in tqdm(directions):
    dir = dLookup[direction]
    robot = np.argwhere(warehouse == "@")[0] #TODO could be made more efficient
    push(robot, dir)
print(warehouse)
print(calcAllGps(warehouse))
