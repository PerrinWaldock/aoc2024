import numpy as np
from collections import deque
import os
from functools import cache

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
    if delta[1] < 0:
        newstart = addtuple(start, (0,-1))
        returnPaths.extend(["<"+p for p in getAllPathsBetween(newstart, end, mapkey)])
    if delta[0] > 0:
        newstart = addtuple(start, (1,0))
        returnPaths.extend(["v"+p for p in getAllPathsBetween(newstart, end, mapkey)])
    if delta[0] < 0:
        newstart = addtuple(start, (-1,0))
        returnPaths.extend(["^"+p for p in getAllPathsBetween(newstart, end, mapkey)])
    if delta[1] > 0:
        newstart = addtuple(start, (0,1))
        returnPaths.extend([">"+p for p in getAllPathsBetween(newstart, end, mapkey)])
    return returnPaths

def countChanges(sequence):
    if len(sequence) == 1:
        return 0
    changes = 0
    previous = sequence[0]
    for s in sequence[1:]:
        if s != previous:
            changes += 1
        previous = s
    return changes

def getShortestSequences(sequences):
    if len(sequences) == 0:
        return sequences
    minlength = min([len(s) for s in sequences])
    return [s for s in sequences if len(s) == minlength]

def getFewestChanges(sequences):
    if len(sequences) == 0:
        return sequences
    fewestChanges = min(countChanges(s) for s in sequences)
    return [s for s in sequences if countChanges(s) == fewestChanges]

@cache
def getBestPathBetween(start, end, mapkey):
    if start == end:
        return "A"
    paths = getAllPathsBetween(start, end, mapkey)
    paths = getShortestSequences(paths)
    paths = getFewestChanges(paths)
    return paths[0]

@cache
def getBestPathBetweenSymbols(startsymbol, endsymbol, mapkey):
    start = lookups[mapkey][startsymbol]
    end = lookups[mapkey][endsymbol]
    return getBestPathBetween(start, end, mapkey)

def getShortestPathForSequence(sequence, mapkey, startsymbol="A"):
    newsequence = []
    for nextsymbol in sequence:
        path = getBestPathBetweenSymbols(startsymbol, nextsymbol, mapkey)
        startsymbol = nextsymbol
        newsequence.append(path)
    return "".join(newsequence)

def getSequenceForKeypad(sequence):
    return getShortestPathForSequence(sequence, "keypad")

@cache
def getCharsForArrows(start, next, robots, startsymbol="A"):
    sequence = getBestPathBetweenSymbols(start, next, "arrows")
    if robots == 1:
        return len(sequence)
    
    sum = 0
    for c in sequence:
        sum += getCharsForArrows(startsymbol, c, robots-1)
        startsymbol = c
    return sum

def getUserCharsLength(sequence, robots, startsymbol="A"):
    keypadsequence = getSequenceForKeypad(sequence)
    
    sum = 0
    for c in keypadsequence:
        sum += getCharsForArrows(startsymbol, c, robots)
        startsymbol = c
    return sum

filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input.txt")
# filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample.txt")

with open(filename) as f:
    sequences = [line.strip() for line in f.readlines()]

def getSequenceNumber(line):
    return int(line.replace("A", ""))

def calcSequenceComplexity(sequence):
    commands = getUserCharsLength(sequence, 25)
    number = getSequenceNumber(sequence)
    return number*commands

sum = 0
for sequence in sequences:
    sum += calcSequenceComplexity(sequence)
print(sum)