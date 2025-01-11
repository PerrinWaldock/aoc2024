from collections import deque
import os

filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input.txt")
#filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample.txt")

rules = deque()
updates = deque()
with open(filename) as f:
	for line in f:
		line = line.strip()
		if "|" in line:
			rules.append([int(x) for x in line.split("|")])
		elif len(line) > 0:
			updates.append([int(x) for x in line.split(",")])

rulesdict = {k: deque() for k,v in rules}
for k,v in rules:
    rulesdict[k].append(v)
rulesdict = {k: set(v) for k,v in rulesdict.items()}

def checkIfLineValid(pages):
	valid = True
	for a, b in rules:
		if a in pages and b in pages and pages.index(a) >= pages.index(b):
			valid = False
			break
	return valid

def comparator(a, b):
	if a in rulesdict and b in rulesdict[a]:
		return -1
	elif b in rulesdict and a in rulesdict[b]:
		return 1
	else:
		return 0
		
from functools import cmp_to_key
def fixLine(pages):
	return sorted(pages, key=cmp_to_key(comparator))

sum = 0
for update in updates:
	if not checkIfLineValid(update):
		newupdate = fixLine(update)
		sum += newupdate[len(newupdate)//2]
print(sum)