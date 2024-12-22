import numpy as np
from collections import deque
import re
import os
from tqdm import tqdm
import itertools

filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input.txt")
filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample.txt")

lines = deque()
with open(filename) as f:
	for line in f:
		lines.append(line)