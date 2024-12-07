import numpy as np
from collections import deque
import re
import os
from tqdm import tqdm

filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input.txt")
#filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample.txt")
    

values = deque()
numbers = deque()
with open(filename) as f:
	for line in f:
		value, nums = line.split(":")
		value = int(value.strip())
		nums = [int(n.strip()) for n in nums.split()]
		values.append(value)
		numbers.append(nums)

def returnPossibleNumbers(nums):
    if len(nums) > 1:
        subnums = returnPossibleNumbers(nums[:-1])
        retval = [nums[-1]*n for n in subnums] + [nums[-1]+n for n in subnums] + [int(str(n)+str(nums[-1])) for n in subnums]
    else:
        retval = [nums[-1]]
    return retval

def isValidLine(val, nums):
    possibilities = returnPossibleNumbers(nums)
    return val in possibilities
    
sum = 0
for val, nums in tqdm(zip(values, numbers), total=len(values)):
    if isValidLine(val, nums):
        sum += val
print(sum)