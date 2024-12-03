import numpy as np
from collections import deque
import re
import os

filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input.txt")
filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample.txt")

lines = deque()
with open(filename) as f:
    for line in f:
        splitline = re.split(r'\s+', line)
        lines.append([int(x) for x in splitline if x != ''])

lines = np.array(lines)
for columnInd in range(np.shape(lines)[1]):
    lines[:,columnInd] = sorted(lines[:,columnInd])
    
print(np.sum(np.abs(lines[:,1] - lines[:,0])))