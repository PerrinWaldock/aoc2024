from collections import deque
import os
import itertools
from functools import cache
import re

# 2311 is too high

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
    
    def getCombosOf(keys, n=3):
        return [tuple(sorted(c)) for c in itertools.combinations(keys, n)]

    @cache
    def areNodesConnected(keys):
        for k in keys:
            connections = nodes[k]
            for sk in keys:
                if sk != k and not sk in connections:
                    return False
        return True

    def findIntersectionOfConnected(k):
        retval = set()
        for combo in getCombosOf(selfconnectednodes[k]):
            if areNodesConnected(combo):
                retval.add(combo)
        return retval
    
    connected = set()
    for node in nodes:
        newconnected = findIntersectionOfConnected(node)
        if len(newconnected) > 0:
            connected |= newconnected
    
    validconnected = set()
    for conn in connected:
        if any("t" == c[0] for c in conn):
            validconnected.add(conn)
    print(len(validconnected))         
    # printSets(validconnected)
    
    
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