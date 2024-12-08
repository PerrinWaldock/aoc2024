import numpy as np
from collections import deque
import re
import os
from tqdm import tqdm
import itertools

filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input.txt")
#filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample.txt")
	

lines = deque()
with open(filename) as f:
	for line in f:
		lines.append([c for c in line.strip()])
array = np.array(lines)

nodes = [[deque() for i in range(np.shape(array)[1])] for j in range(np.shape(array)[0])]

characters = [c for c in set(np.ravel(array)) if c != "."]

def inRange(n):
	return 0 <= n[0] < np.shape(array)[0] and 0 <= n[1] < np.shape(array)[1]

def nodesForPair(a, b):
	retlist = list()
	diff = a - b
	
	node1 = a
	node2 = b
	
	multiplier = 0
	while inRange(node1) or inRange(node2):
		if inRange(node1):
			retlist.append(tuple(node1))
		if inRange(node2):
			retlist.append(tuple(node2))
		multiplier += 1
		node1 = a + multiplier*diff
		node2 = b - multiplier*diff
   
	return retlist

def findNodes(arr, c):
	towers = np.argwhere(arr == c)
	nodes = deque()
	pairs = itertools.combinations(towers, 2)
	for pair in pairs:
		nodes.extend(nodesForPair(*pair))
	return set(nodes)
	
nodes = set()
for c in characters:
	ns = findNodes(array, c)
	for n in ns:
		nodes.add(n)
print(len(nodes))