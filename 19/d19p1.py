import numpy as np
from collections import deque
import re
import os
from tqdm import tqdm
import itertools
import sys

import dataclasses
from typing import Any

filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input.txt")
# filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample.txt")

arrangements = deque()
with open(filename) as f:
    for ind, line in enumerate(f):
        if ind == 0:
            towels = [t.strip() for t in line.split(",")]
        elif line.strip() != "":
            arrangements.append(line.strip())
            
def findTowelSequence(sequence):
    for towel in towels:
        if sequence.startswith(towel):
            if sequence == towel:
                return [towel]
            else:
                restOfSequence = findTowelSequence(sequence[len(towel):])
                if restOfSequence is None:
                    continue
                else:
                    return [towel] + restOfSequence
    return None

valid = 0
for arrangement in arrangements:
    sequence = findTowelSequence(arrangement)
    if sequence is not None:
        valid += 1
print(valid)