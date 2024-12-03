import numpy as np
from collections import deque
import re
import os

filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input.txt")
#filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample2.txt")

GOOD = "do()"
BAD = "don't()"

lines = deque()
with open(filename) as f:
    text = f.read()
    
    output = deque()
    matches = list(re.finditer(r"do\(\)|don't\(\)", text))
    good = True
    lastind = 0
    
    for match in matches:
        if good:
            output.append(text[lastind:match.span()[0]])
            
        if match.group() == "do()":
            good = True
        elif match.group() == "don't()":
            good = False
        
        lastind = match.span()[1]
    
    if good:
        output.append(text[lastind:])
    
    text = "".join(output)
    
    sum = 0
    for match in re.findall(r"mul\([0-9]{1,3},[0-9]{1,3}\)", text):
        numbers = [int(s) for s in re.findall(r"[0-9]{1,3}", match)]
        sum += numbers[0]*numbers[1]

print(sum)
    