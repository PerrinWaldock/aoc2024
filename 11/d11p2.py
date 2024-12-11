import numpy as np
from collections import deque
import re
import os
from tqdm import tqdm
import itertools
from functools import cache

filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input.txt")
#filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample.txt")
#filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample2.txt")

blinks = 75

with open(filename) as f:
	lines = f.readlines()
	line = "".join(lines).split(" ")
	line = [int(c) for c in line]
array = np.array(line)

@cache
def stonesAfterIterations(a, i):
	if i == 0:
		return 1
	stra = str(a)
	if a == 0:
		return stonesAfterIterations(1, i-1)
	elif len(stra)%2 == 0:
		return stonesAfterIterations(int(stra[:len(stra)//2]), i-1) + stonesAfterIterations(int(stra[len(stra)//2:]), i-1)
	else:
		return stonesAfterIterations(a*2024, i-1)

sum = 0
for a in array:
	stones = stonesAfterIterations(a, blinks)
	sum += stones
print(sum)