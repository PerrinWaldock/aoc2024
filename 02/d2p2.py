import numpy as np
from collections import deque
import re
import os

filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input.txt")
#filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample.txt")

lines = deque()
with open(filename) as f:
    for line in f:
        splitline = re.split(r'\s+', line)
        lines.append([int(x) for x in splitline if x != ''])
        
def isSafe(xs):
    diff = np.diff(xs)
    return (np.all(diff > 0) and np.all(diff < 4)) or (np.all(diff < 0) and np.all(diff > -4))

safecount = 0
for line in lines:
    #print(line)
    for ind in range(len(line)):
        newline = line[:ind] + line[ind+1:]
        #print("  ", newline)
        if isSafe(newline):
            safecount += 1
            break
    
#475 too low        
print(safecount)