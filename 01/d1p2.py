import numpy as np
from collections import deque, Counter
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

rightOccurances = Counter(lines[:,1])
leftOccurances = Counter(lines[:,0])
score = 0
for leftOccurance, count in leftOccurances.items():
    if leftOccurance in rightOccurances:
        score += leftOccurance*rightOccurances[leftOccurance]*count
        
#could make it simpler by just counting occurances of left and right
    
print(score)
# 18997088