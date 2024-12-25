import numpy as np
from collections import deque
import re
import os
from tqdm import tqdm
import itertools

import dataclasses
from typing import Any

ACOST = 3
BCOST = 1
CORRECTION = 10000000000000

filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input.txt")
# filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample.txt")

def getCoefficientsFromLine(line):
    return [int(n) for n in re.findall(r'\d+', line)]

@dataclasses.dataclass
class State:
    ax: int = None
    ay: int = None
    bx: int = None
    by: int = None
    X: int = None
    Y: int = None

def isFilled(s):
    s = dataclasses.astuple(s)
    return len(s) == len([p for p in s if p is not None])

state = State()
infos = deque()
with open(filename) as f:
    for line in f:
        if "Button A" in line:
            nums = getCoefficientsFromLine(line)
            state.ax = nums[0]
            state.ay = nums[1]
        if "Button B" in line:
            nums = getCoefficientsFromLine(line)
            state.bx = nums[0]
            state.by = nums[1]
        if "Prize" in line:
            nums = getCoefficientsFromLine(line)
            state.X = nums[0] + CORRECTION
            state.Y = nums[1] + CORRECTION
        if isFilled(state):
            infos.append(state)
            state = State()
        
def solveState(s):
    a = [[s.ax, s.bx],[s.ay, s.by]]
    b = [s.X, s.Y]
    sln = np.linalg.solve(a, b)
    return sln

def solveStatePrecise(s):
    determinant = 1/(s.ax*s.by - s.ay*s.bx)
    slnx = determinant*(s.by*s.X - s.bx*s.Y)
    slny = determinant*(-s.ay*s.X + s.ax*s.Y)
    return (slnx, slny)

def isInteger(x):
    return np.abs(x - round(x)) < 1e-3

def processState(s):
    sln = solveStatePrecise(s)
    if all([isInteger(n) for n in sln]) and all(n >= 0 for n in sln):
        return round(sln[0]*ACOST + sln[1]*BCOST)
    else:
        return None
   
presses = 0 
for state in infos:
    press = processState(state)
    if press is not None:
        presses += press
print(presses)