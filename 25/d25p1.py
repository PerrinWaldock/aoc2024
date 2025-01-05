import numpy as np
from collections import deque, namedtuple, Counter
import re
import os
from tqdm import tqdm
import itertools
import sys
from functools import cache
import re
import dataclasses
from typing import Any

MAX_HEIGHT = 5

def main():
    filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input.txt")
    # filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample.txt")       
    
    schematics = deque()
    with open(filename) as f:
        schematic = deque()
        for line in f:
            line = line.strip()
            if line == "":
                schematics.append(np.array(schematic))
                schematic = deque()
                continue
            schematic.append([c for c in line])
        if line != "" and len(schematic) != 0:
            schematics.append(np.array(schematic))
    
    keys = deque()
    locks = deque()
    for schematic in schematics:
        heights = tuple([Counter(c)["#"] - 1 for c in np.transpose(schematic)])
        if set(schematic[0]) == {"#"}:
            locks.append(heights)
        elif set(schematic[-1]) == {"#"}:
            keys.append(heights)
    
    keys = set(keys)
    locks = set(locks)
    
    totalfits = 0
    for key in keys:
        for lock in locks:
            if fits(key, lock):
                totalfits += 1
    print(totalfits)

def fits(key, lock):
    return all(k + l <= MAX_HEIGHT for k, l in zip(key, lock))

if __name__ == "__main__":
    main()