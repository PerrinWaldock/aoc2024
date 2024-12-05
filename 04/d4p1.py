import numpy as np
from collections import deque
import re
import os

#filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input.txt")
filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample.txt")

lines = deque()
with open(filename) as f:
    for line in f:
        lines.append(list(line.replace("\n", "")))
arr = np.array(lines)
tarr = np.transpose(arr)
farr = np.flip(arr, axis=0)
tfarr = np.transpose(farr)

def addReverse(xs):
    return list(xs) + [list(x)[::-1] for x in xs]

lines = deque()
horizontalLines = [row for row in arr]
horizontalLines = addReverse(horizontalLines)
verticalLines = [row for row in tarr]
verticalLines = addReverse(verticalLines)

diagonalLines = deque()
for ind, x in enumerate(range(max(np.shape(arr)))):
    diagonalLines.append(np.diagonal(arr, x))
    if ind > 0:
	    diagonalLines.append(np.diagonal(tarr, x))
diagonalLines = addReverse(diagonalLines)

antidiagonalLines = deque()
for ind, x in enumerate(range(max(np.shape(farr)))):
    antidiagonalLines.append(np.diagonal(farr, x))
    if ind > 0:
	    antidiagonalLines.append(np.diagonal(tfarr, x))
antidiagonalLines = addReverse(antidiagonalLines)

lines.extend(horizontalLines)
lines.extend(verticalLines)
lines.extend(diagonalLines)
lines.extend(antidiagonalLines)

count = 0
for line in lines:
    line = "".join(line)
    count += len(re.findall("XMAS", line))
    
print(count)
# todo missing other diagonal

    

