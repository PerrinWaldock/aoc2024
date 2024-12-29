import numpy as np
from collections import deque
import re
import os
from tqdm import tqdm
import itertools
import sys
from functools import cache

import dataclasses
from typing import Any

keypad = np.array([	['7', '8', '9'],
                      ['4', '5', '6'],
                          ['1', '2', '3'],
                      ['', '0', 'A']])
arrows = np.array([['', '^', 'A'],
                   ['<', 'v', '>']])

def createLookup(arr):
    symbols = set(np.ravel(arr))
    return {s: tuple(np.argwhere(arr == s)[0]) for s in symbols}

maps = {"keypad": keypad, "arrows": arrows}
lookups = {k: createLookup(v) for k,v in maps.items()}

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

@cache
def getAllPathsBetweenSymbols(startsymbol, endsymbol, mapkey):
    start = lookups[mapkey][startsymbol]
    end = lookups[mapkey][endsymbol]
    return getAllPathsBetween(start, end, mapkey)

#should be list of lists of strings corresponding to potential paths
"""
11 21 31
12 22 32
13 23 33

return 112131, 112132, 113233, 112231, etc...
"""
def getAllSequentialCombosFrom2dList(l):
    if len(l) == 1:
        return l[0]
    subsequentCombos = getAllSequentialCombosFrom2dList(l[1:])
    combos = []
    for option in l[0]:
        for subsequentCombo in subsequentCombos:
            combos.append(option+subsequentCombo)
    return combos

def getShortestSequences(sequences):
    minlength = min([len(s) for s in sequences])
    return [s for s in sequences if len(s) == minlength]

#TODO this may soon become intractable
@cache
def getAllShortestPathsForSequence(sequence, mapkey, startsymbol="A"): #TODO make sure that first element of sequence is 
    keysequences = [] #will hold a list of possible shortest paths
    for nextsymbol in sequence:
        paths = getAllPathsBetweenSymbols(startsymbol, nextsymbol, mapkey) #list of paths between symbols
        startsymbol = nextsymbol
        keysequences.append(paths)
    #answer could be ANY combination of these paths in order :(
    possibleSequences = getAllSequentialCombosFrom2dList(keysequences)
    return getShortestSequences(possibleSequences)

def getUserSequences(sequence):
    usersequences = []
    keypadsequences = getAllShortestPathsForSequence(sequence, "keypad")
    for keypadsequence in keypadsequences:
        robot1sequences = getAllShortestPathsForSequence(keypadsequence, "arrows")
        for robot1sequence in robot1sequences:
            robot2sequences = getAllShortestPathsForSequence(robot1sequence, "arrows")
            usersequences.extend(robot2sequences)
    return getShortestSequences(usersequences)

filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input.txt")
# filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample.txt")

with open(filename) as f:
    sequences = [line.strip() for line in f.readlines()]

def getSequenceNumber(line):
    return int(line.replace("A", ""))

def calcSequenceComplexity(sequence):
    commands = getUserSequences(sequence)[0]
    number = getSequenceNumber(sequence)
    print(sequence, number, len(commands))
    return number*len(commands)

sum = 0
for sequence in sequences:
    sum += calcSequenceComplexity(sequence)
print(sum)