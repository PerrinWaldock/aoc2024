import numpy as np
from collections import deque
import re
import os

filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input.txt")
#filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample.txt")

lines = deque()
with open(filename) as f:
	for line in f:
		lines.append(list(line.replace("\n", "")))
arr = np.array(lines)

def isXmas(a):
    return a[0,0] == "M" and a[2,0] == "M" and a[1,1] == "A" and a[0,2] == "S" and a[2,2] == "S"

def countXmas(xs):
	count = 0
	for ind in range(np.shape(xs)[1]-2):
		for jnd in range(np.shape(xs)[0]-2):
			a = xs[ind:ind+3,jnd:jnd+3]
			permutations = [a, np.rot90(a, k=1), np.rot90(a, k=2), np.rot90(a, k=3)]
			for perm in permutations:
				if isXmas(perm):
					count += 1
	return count

count = countXmas(arr)
print(count)