import numpy as np
from collections import deque, namedtuple
import re
import os
from tqdm import tqdm
import itertools
import sys
from functools import cache
import re
import dataclasses
from typing import Any

def main():
    filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input.txt")
    #filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample.txt")
    #filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample2.txt")
    
    Gate = namedtuple('Gate', ['in1', 'in2', 'op', 'out'])
    
    wires = {}
    gates = {}
    with open(filename) as f: 
        for line in f:
            if ":" in line:
                key, value = line.split(":")
                wires[key] = int(value.strip())
            if "->" in line:
                inputs, output = line.split("->")
                output = output.strip()
                in1, operator, in2 = inputs.strip().split()
                gates[output] = Gate(in1, in2, operator, output)

    gatesToResolve = sorted([gate for gate in gates if gate[0] == "z"], key = lambda n: int(n[1:]))
 
    def resolveGate(g):
        gate = gates[g]
        if not gate.in1 in wires:
            resolveGate(gate.in1)
        if not gate.in2 in wires:
            resolveGate(gate.in2)
            
        in1 = wires[gate.in1]
        in2 = wires[gate.in2]
        
        if gate.op == "AND":
            wires[gate.out] = in1 and in2
        if gate.op == "OR":
            wires[gate.out] = in1 or in2
        if gate.op == "XOR":
            wires[gate.out] = in1 ^ in2
    
    for gate in gatesToResolve:
        resolveGate(gate)
        
    number = 0
    for ind, name in enumerate(gatesToResolve):
        gate = gates[name]
        number += wires[gate.out] << ind
        print(name, wires[gate.out])
    print(number)
                    
if __name__ == "__main__":
    main()