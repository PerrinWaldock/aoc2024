from collections import deque
import os
from functools import cache

filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input.txt")
# filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample.txt")

arrangements = deque()
with open(filename) as f:
    for ind, line in enumerate(f):
        if ind == 0:
            towels = [t.strip() for t in line.split(",")]
        elif line.strip() != "":
            arrangements.append(line.strip())

@cache
def countTowelSequences(sequence):
    totalSequences = 0
    for towel in towels:
        if sequence.startswith(towel):
            if sequence == towel:
                totalSequences += 1
            else:
                totalSequences += countTowelSequences(sequence[len(towel):])
    return totalSequences

sequences = 0
for arrangement in arrangements:
    sequences += countTowelSequences(arrangement)
print(sequences)