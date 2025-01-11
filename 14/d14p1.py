import numpy as np
from collections import deque
import re
import os

import dataclasses

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

robots = deque()
with open(filename) as f:
    for line in f:
        ns = getIntsFromLine(line)
        robots.append(Robot(*ns))

for robot in robots:
    robot.iterate(ITERATIONS)
    
sums = deque()
for quadrant in getQuadrants(WIDTH-1,HEIGHT-1):
    sums.append(getRobotsIn(robots, *quadrant))
print(sums)
print(np.product(sums))

#TODO print out picture of each of the robots, see if it forms anything christmas-tree like after each step?