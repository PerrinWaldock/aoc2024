import numpy as np
from collections import deque
import os

filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input.txt")
#filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample.txt")
#filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample2.txt")
	
with open(filename) as f:
	line = [int(c) for c in ''.join(f.readlines())]
line.append(0)

disk = deque()
allblocks = deque()
for id, (blocks, freespace) in enumerate(zip(line[::2], line[1::2])):
	disk.extend([id]*blocks)
	disk.extend([-1]*freespace)
	allblocks.append(blocks)
disk = np.array(disk)
totaldiskspace = np.sum(allblocks)

freespots = list(np.argwhere(disk == -1))
filledspots = reversed(list(np.argwhere(disk >= 0)))
for freeind, filledind in zip(freespots, filledspots):
    if freeind > filledind:
        break
    disk[freeind] = disk[filledind]
disk = disk[:totaldiskspace]
checksum = np.sum(disk*np.arange(len(disk)))
print(checksum)