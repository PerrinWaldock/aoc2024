import numpy as np
from collections import deque
import os
from tqdm import tqdm

# would be faster to only store the disk as a number of contiguous blocks

filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input.txt")
#filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample.txt")
#filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample2.txt")
	
with open(filename) as f:
	line = [int(c) for c in ''.join(f.readlines())]
line.append(0)

disk = deque()
allblocks = deque()
ids = deque()
locations = deque()
locations.append(0)
for id, (blocks, freespace) in enumerate(zip(line[::2], line[1::2])):
	disk.extend([id]*blocks)
	disk.extend([-1]*freespace)
	allblocks.append(blocks)
	ids.append(id)
	locations.append(locations[-1]+blocks+freespace)
disk = np.array(disk)
totaldiskspace = np.sum(allblocks)
allblocks = list(allblocks)
locations = list(locations)

def findFirstSpaceLargerThan(d, s):
	startInd = -1
	for ind in range(len(d)):
		if d[ind] < 0:
			if ind - startInd >= s:
				return startInd + 1
		else:
			startInd = ind
	return len(disk)

def findSizeOf(d, id):
	inds = np.argwhere(d == id)
	return min(inds), len(inds)

def moveBlocks(d, sourceId, endId, blocks):
	d[endId:endId+blocks] = d[sourceId:sourceId+blocks]
	d[sourceId:sourceId+blocks] = -1*np.ones(blocks)
	return d

for id in tqdm(reversed(ids), total=len(ids)):
	startInd = locations[id]
	neededsize = allblocks[id]
	newloc = findFirstSpaceLargerThan(disk, neededsize)
	if newloc < startInd:
		disk = moveBlocks(disk, startInd, newloc, neededsize)

disk[disk < 0] = 0

checksum = np.sum(disk*np.arange(len(disk)))
print(checksum)