import numpy as np
from collections import deque
import re
import os
from tqdm import tqdm
import itertools
import sys
from functools import cache
import re
import dataclasses
from typing import Any

"""
TODO
	# have set of explored nodes
	# search from one node, recusive call or loop to unexplored nodes in frontier set
	# 	if no more nodes can be explored from that node, return a set of it
	# 	otherwise, return recursive call + current node
	# once a connected set is found, start a new recursive function. Return largest
	^^^ not valid because need direct connections
"""

#not du,eq,iw,ol,sd,tl,tt,ub,wd,wg,xl,yq

def main():
    filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input.txt")
    # filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample.txt")
    
    pairs = deque()
    with open(filename) as f: 
        for line in f:
            pairs.append(tuple(line.strip().split("-")))
    
    nodes = dict()
    for a, b in pairs:
        if not a in nodes:
            nodes[a] = set()
        nodes[a].add(b)
        
        if not b in nodes:
            nodes[b] = set()
        nodes[b].add(a)
    selfconnectednodes = {k: addAndCopySet(v, k) for k, v in nodes.items()}
    
    biggestCombo = 1
    def getCombos(keys):
        combos = []
        for n in range(biggestCombo, len(keys)):
            combos.extend(getCombosOf(tuple(keys), n))
        return combos
    
    @cache
    def getCombosOf(keys, n):
        return [tuple(sorted(c)) for c in itertools.combinations(keys, n)] # if any(n[0] == 't' for n in c) looks like the "t" requirement no longer holds

    @cache
    def areNodesConnected(keys):
        for k in keys:
            connections = nodes[k]
            for sk in keys:
                if sk != k and not sk in connections:
                    return False
        return True

    def findIntersectionOfConnected(k):
        global biggestCombo
        retval = set()
        for combo in getCombos(selfconnectednodes[k]):
            if areNodesConnected(combo):
                biggestCombo = len(combo)
                retval.add(combo)
        return retval
    
    connected = set()
    for node in tqdm(nodes):
        newconnected = findIntersectionOfConnected(node)
        if len(newconnected) > 0:
            connected |= newconnected
    
    connected = list(connected)
    biggestconnected = max(connected, key = lambda c: len(c))
    print(','.join(biggestconnected))
    
    
def printSets(sets):
    connlist = sorted([','.join(sorted(con)) for con in sets])
    for conn in connlist:
        print(conn)
    
def addAndCopySet(s, a):
    copyset = s.copy()
    copyset.add(a)
    return copyset

if __name__ == "__main__":
    main()