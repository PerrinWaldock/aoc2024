import numpy as np
from collections import deque
import os
from tqdm import tqdm

filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input.txt")
#filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample.txt")
#filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample2.txt")

blinks = 25

with open(filename) as f:
	lines = f.readlines()
	line = "".join(lines).split(" ")
	line = [int(c) for c in line]
array = np.array(line)

def evolveLine(arr):
	output = deque()
	for a in arr:
		stra = str(a)
		if a == 0:
			output.append(1)
		elif len(stra)%2 == 0:
			output.append(int(stra[:len(stra)//2]))
			output.append(int(stra[len(stra)//2:]))
		else:
			output.append(a*2024)
	return output

for blink in tqdm(range(blinks), total=blinks):
	array = evolveLine(array)
print(len(array))