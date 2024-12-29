import numpy as np
from collections import deque
import re
import os
from tqdm import tqdm
import itertools
import sys
from functools import cache

"""
TODO revert to previous version (see github), but add different path finding for keypad vs arrows
"""

import dataclasses
from typing import Any

keypad = np.array([	['7', '8', '9'],
                      ['4', '5', '6'],
                          ['1', '2', '3'],
                      ['', '0', 'A']])
arrows = np.array([['', '^', 'A'],
                   ['<', 'v', '>']])

maps = {"keypad": keypad, "arrows": arrows}

def createLookup(arr):
    symbols = set(np.ravel(arr))
    return {s: tuple(np.argwhere(arr == s)[0]) for s in symbols}

def addtuple(a, b):
    return (a[0]+b[0], a[1]+b[1])

def subtracttuple(a, b):
    return (a[0]-b[0], a[1]-b[1])

def getDistance(a, b):
    return int(np.abs(a[0]-b[0]) + np.abs(a[1]-b[1]))

#TODO may be able to just pick a best path?
@cache
def getAllPathsBetween(start, end, mapkey):
    if maps[mapkey][*start] == "" or maps[mapkey][*end] == "":
        return []
    elif start == end:
        return ["A"]
    delta = subtracttuple(end, start)
    returnPaths = deque()
    if delta[0] > 0:
        newstart = addtuple(start, (1,0))
        returnPaths.extend(["v"+p for p in getAllPathsBetween(newstart, end, mapkey)])
    elif delta[0] < 0:
        newstart = addtuple(start, (-1,0))
        returnPaths.extend(["^"+p for p in getAllPathsBetween(newstart, end, mapkey)])
    if delta[1] > 0:
        newstart = addtuple(start, (0,1))
        returnPaths.extend([">"+p for p in getAllPathsBetween(newstart, end, mapkey)])
    elif delta[1] < 0:
        newstart = addtuple(start, (0,-1))
        returnPaths.extend(["<"+p for p in getAllPathsBetween(newstart, end, mapkey)])
    return returnPaths    

class Robot:
    def __init__(self, mapkey, startsymbol='A'):
        self.mapkey = mapkey
        self.lookup = createLookup(maps[mapkey])
        self.position = self.lookup[startsymbol]
    
    #turns number or arrow into sets of sequences of arrows.
    def getAllCommandsTo(self, symbol):
        destination = self.lookup[symbol]
        retval = getAllPathsBetween(self.position, destination, self.mapkey)
        self.position = destination
        return retval
    
    #don't want to do all at once because many extra paths will be generated

#TODO this can be modified to be cached?
@cache
def getShortestCommandsForSymbol(robots, symbol):
    commandsequences = robots[0].getAllCommandsTo(symbol)
    if len(robots) == 1:
        return commandsequences
    newsequences = []
    for sequence in commandsequences:
        for s in sequence:
            newsequences.extend(getShortestCommandsForSymbol(robots[1:], s)) #TODO need to think VERY carefully about whether robot positions are being preserved correctly
    shortestlength = min([len(sequence) for sequence in newsequences])
    return [sequence for sequence in newsequences if len(sequence) == shortestlength]

def getShortestCommandsForSequence(robots, sequence):
    #TODO do the same as above but for the full sequence
    #TODO think carefully about whether robot positions are preserved. Start and End are the same, but will the middles cause problems?
    #need to reset robot positions after each?
    possiblesequences = []
    for s in sequence:
        possiblesequences.append(getShortestCommandsForSymbol(robots, s))
    #count min length for each sequence?

keypadbot = Robot("keypad")
arrowbot1 = Robot("arrows")
arrowbot2 = Robot("arrows")

robots = (keypadbot, arrowbot1, arrowbot2)



filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input.txt")
filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample.txt")

with open(filename) as f:
    sequences = [line.strip() for line in f.readlines()]

def getSequenceNumber(line):
    return int(line.replace("A", ""))

def calcSequenceComplexity(sequence):
    commands = rc.getCommandsForSequence(sequence)
    number = getSequenceNumber(sequence)
    print(sequence, number, len(commands))
    return number*len(commands)

sum = 0
for sequence in sequences:
    sum += calcSequenceComplexity(sequence)
print(sum)

#TODO need to make several fixes:
# need to make sure that the robot does not pass over the gap -- have one wayfinder for the keypad and one for the arrows
# need to return all possible shortest routes rather than just one
# robots need to consider all possible routes rather than just one, return all possible shortest