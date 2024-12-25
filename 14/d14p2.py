import numpy as np
from collections import deque
import re
import os
from tqdm import tqdm
import itertools

import dataclasses
from typing import Any

filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input.txt")
# filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample.txt")

ITERATIONS = 100
if "sample" in filename:
    WIDTH = 11
    HEIGHT = 7
elif "input" in filename:
    WIDTH = 101
    HEIGHT = 103
    
@dataclasses.dataclass
class Robot:
    x: int = None
    y: int = None
    vx: int = None
    vy: int = None
    
    def iterate(self, n=1):
        self.x = (self.x + self.vx*n)%WIDTH
        self.y = (self.y + self.vy*n)%HEIGHT
    
def getIntsFromLine(line):
    return [int(n) for n in re.findall(r'-?\d+', line)]

def getRobotsIn(robots, minx, miny, maxx, maxy):
    return len([r for r in robots if minx <= r.x <= maxx and miny <= r.y <= maxy])

def getQuadrants(maxx, maxy):
    midx = maxx//2
    midy = maxy//2
    return [(0,0,midx-1,midy-1),
            (0,midy+1,midx-1,maxy),
            (midx+1,0,maxx,midy-1),
            (midx+1,midy+1,maxx,maxy)]

def visualize(robots):
    arr = np.zeros((HEIGHT,WIDTH))
    for r in robots:
        arr[r.y,r.x] += 1
    arr[arr > 9] = 9
    arr = np.char.mod('%d', arr)
    block = ""
    for chars in arr:
        block += "".join(chars) + "\n"
    block = block.replace("0", ".")
    return block

def getBotsInQuadrant(robots):
    sums = deque()
    for quadrant in getQuadrants(WIDTH-1,HEIGHT-1):
        sums.append(getRobotsIn(robots, *quadrant))
    return sums

robots = deque()
with open(filename) as f:
    for line in f:
        ns = getIntsFromLine(line)
        robots.append(Robot(*ns))

images = set()
iteration = 0
while iteration < 15000:
    sums = getBotsInQuadrant(robots)
    if any(np.array(sums) > 250):
        print(iteration)
        image = visualize(robots)
        print(image)
    for robot in robots:
        robot.iterate()
    iteration += 1
    

#TODO print out picture of each of the robots, see if it forms anything christmas-tree like after each step?
# the pattern may repeat at 10403? we at least see duplicate positions
# may just want to count number of robots in a space to see when they get dense enough to form a tree?