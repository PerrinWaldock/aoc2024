from collections import deque
import re
import os

filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input.txt")
#filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample.txt")

lines = deque()
with open(filename) as f:
    text = f.read()
    sum = 0
    for match in re.findall(r"mul\([0-9]{1,3},[0-9]{1,3}\)", text):
        numbers = [int(s) for s in re.findall(r"[0-9]{1,3}", match)]
        sum += numbers[0]*numbers[1]

print(sum)
    