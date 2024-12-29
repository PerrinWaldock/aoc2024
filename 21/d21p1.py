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

def addtuple(a, b):
    return (a[0]+b[0], a[1]+b[1])
def subtracttuple(a, b):
    return (a[0]-b[0], a[1]-b[1])

#TODO create lookup for distances + keys

def getDistance(a, b):
    return int(np.abs(a[0]-b[0]) + np.abs(a[1]-b[1]))

@cache
def getCommandsForDelta(delta):
    directions = ""
    if delta[0] > 0:
        directions += "v"*delta[0]
    elif delta[0] < 0:
        directions += "^"*-delta[0]
    if delta[1] > 0:
        directions += ">"*delta[1]
    elif delta[1] < 0:
        directions += "<"*-delta[1]
    return directions + "A"

class Robot:
    def __init__(self, array, startsymbol='A'):
        self.array = array
        self.lookup = createLookup(array)
        self.position = self.lookup[startsymbol]
    
    #turns number or arrow into sequence of arrows
    def getCommandsTo(self, symbol):
        destination = self.lookup[symbol]
        delta = subtracttuple(destination, self.position)
        self.position = destination
        return getCommandsForDelta(delta)
    
    def getCommandsForSequence(self, sequence):
        return ''.join([self.getCommandsTo(s) for s in sequence])
    
    
class RobotCollection:
    def __init__(self, robots):
        self.robots = robots
    
    def getCommandsForSequence(self, sequence):
        for robot in self.robots:
            sequence = robot.getCommandsForSequence(sequence)
        return sequence

keypadbot = Robot(keypad)
arrowbot1 = Robot(arrows)
arrowbot2 = Robot(arrows)

rc = RobotCollection([keypadbot, arrowbot1, arrowbot2])



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