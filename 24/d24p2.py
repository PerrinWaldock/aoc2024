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

    
Gate = namedtuple('Gate', ['in1', 'in2', 'op', 'out'])
gates = {} #hashed by output
gatelookup = {} #set of gates connected to this input

def main():
    filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input.txt")
    #filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample.txt")
    #filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample2.txt")
    #filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample3.txt")
    
    wires = {}
    allwires = set()
    global gates, gatelookup
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
                allwires.add(in1)
                allwires.add(in2)
                allwires.add(output)
    suspects = checkAdders()
    swapPairs = getPairs(suspects)
    for pair in swapPairs:
        print("Swapping", *pair)
        swapOutputs(*pair)
    newSuspects = checkAdders()
    if len(newSuspects) == 0:
        print(",".join(sorted(suspects)))
    else:
        print("need to refine code!")

def getPairs(sequence):
    sequence = iter(sequence)
    return [(s, next(sequence)) for s in sequence]

def generateGateLookup(gates):
    gatelookup = {}
    for g in gates.values():     
        if g.in1 not in gatelookup:
            gatelookup[g.in1] = set()
        if g.in2 not in gatelookup:
            gatelookup[g.in2] = set()
        gatelookup[g.in1].add(gates[g.out]) #TODO need to update gatelookup
        gatelookup[g.in2].add(gates[g.out])
    return gatelookup

def numberToDict(x, label, digits):
    return {f"{label}{n:02}": (x >> digits - 1 - n)%2 for n in range(digits)}

def getConnectedGateTypes(g):
    connectedGates = gatelookup[g]
    return set([g.op for g in connectedGates])

def checkAdders():
    global gatelookup
    gatelookup = generateGateLookup(gates)
    carry = None
    suspectOutputs = list()
    
    #TODO check 0th bit
    BITS = 45
    for n in range(1,BITS):
        carry, suspects = checkAdder(n, carry)
        if len(suspects) > 0:
            suspectOutputs.extend(suspects)
    if carry != f"z{BITS:02}":
        suspectOutputs.append(carry)
    return suspectOutputs

def checkAdder(number, c=None):
    """
    are xn and yn connected to xor and and
        is xor connected to xor and and
            is xor connected to output
            is and connected to or
                or's output connected to next carry
                is and's other input equal to the carry
        is and connected to above or
    """
    
    suspectOutputs = []
    
    x = f"x{number:02}"
    y = f"y{number:02}"
    z = f"z{number:02}"
    if gatelookup[x] != gatelookup[y]:
        if set([g.op for g in gatelookup[x]]) != {"XOR", "AND"}:
            print(number, "X suspect", gatelookup[x])
            suspectOutputs.append(list(gatelookup[x])[0].out)
        if set([g.op for g in gatelookup[y]]) != {"XOR", "AND"}:
            print(number, "Y suspect", gatelookup[x])
            suspectOutputs.append(list(gatelookup[y])[0].out)

    firstXor = [g for g in gatelookup[x] if g.op == "XOR"][0]
    firstAnd = [g for g in gatelookup[x] if g.op == "AND"][0]
    
    if getConnectedGateTypes(firstXor.out) != {"XOR", "AND"}:
        print(number, "first XOR", firstXor, "does not connect to XOR and AND", getConnectedGateTypes(firstXor.out))
        suspectOutputs.append(firstXor.out)

    secondXors = [g for g in gatelookup[firstXor.out] if g.op == "XOR"]
    if len(secondXors) == 1:
        secondXor = secondXors[0]
    elif c is not None:
        secondXors = [g for g in gatelookup[c] if g.op == "XOR"]
        secondXor = secondXors[0]
        
    secondAnds = [g for g in gatelookup[firstXor.out] if g.op == "AND"]
    if len(secondAnds) == 1:
        secondAnd = secondAnds[0]
    elif c is not None:
        secondAnds = [g for g in gatelookup[c] if g.op == "AND"]
        secondAnd = secondAnds[0]
    
    if secondXor.out != z:
        print(number, "second XOR does not connect to output", secondXor)
        suspectOutputs.append(secondXor.out)

    if firstAnd.out not in gatelookup or list(gatelookup[firstAnd.out])[0].op != "OR": #TODO fix
        print(number, "first AND does not connect to OR", firstAnd)
        suspectOutputs.append(firstAnd.out)
    
    if secondAnd.out not in gatelookup or list(gatelookup[secondAnd.out])[0].op != "OR":
        print(number, "second AND does not connect to OR", secondAnd)
        suspectOutputs.append(secondAnd.out)
    
    if firstAnd.out in gatelookup and secondAnd.out in gatelookup and list(gatelookup[firstAnd.out])[0] != list(gatelookup[secondAnd.out])[0]:
        print(number, "first and second AND connected to different gates", list(gatelookup[firstAnd.out])[0], list(gatelookup[secondAnd.out])[0])
    
    if secondAnd.out in gatelookup:
        carrywire = list(gatelookup[secondAnd.out])[0].out
    elif firstAnd.out in gatelookup:
        carrywire = list(gatelookup[firstAnd.out])[0].out
    else:
        carrywire = None
    
    if c is not None and (c not in gatelookup or gatelookup[c] != {secondAnd, secondXor}):
        print(number, "bad carry", c)
        suspectOutputs.append(c)
    
    return carrywire, suspectOutputs
    
def swapOutputs(out1, out2):
    g1 = gates[out1]
    g2 = gates[out2]
    gates[out1] = Gate(g2.in1, g2.in2, g2.op, g1.out)
    gates[out2] = Gate(g1.in1, g1.in2, g1.op, g2.out)
    getDependencies.cache_clear()

def compareOutputToExpected(x, y, operation):
    digits = len([gate for gate in gates if gate[0] == "z"])
    xs = numberToDict(x, "x", digits)
    ys = numberToDict(y, "y", digits)
    xs.update(ys)
    output = getOutput(xs)
    
    if operation == "and":
        expected = x & y
    if operation == "add":
        expected = x + y
    return output == expected

def expectedInputDependencies(output):
    digit = int(output[1:])
    outputs = set()
    for n in range(digit+1):
        outputs.add(f"x{n:02}")
        outputs.add(f"y{n:02}")
    return outputs

def getAllDependencies(wires, intermediates=True):
    deps = {}
    for wire in wires:
        deps[wire] = getDependencies(tuple([wire]), getIntermediates=intermediates)
    return deps

def findSuspectOutputs():
    outputs = sorted([gate for gate in gates if gate[0] == "z"], key = lambda n: int(n[1:]))
    suspectoutputs = deque()
    for output in outputs:
        expected = expectedInputDependencies(output)
        deps = getDependencies(tuple([output]), getIntermediates=False)
        if expected != deps:
            suspectoutputs.append(output)
            depsWithIntermediates = getDependencies(tuple([output]), getIntermediates=True)
            print(output, "extra: ", deps - expected, "missing:",  expected - deps)
            print(output, "deps:", deps, depsWithIntermediates)
    return suspectoutputs

@cache
def getDependencies(outputs, getIntermediates=False):
    dependencies = set()
    for output in outputs:
        if output not in gates:
            dependencies.add(output)
            continue
        if getIntermediates:
            dependencies.add(output)
        gate = gates[output]
        dependencies |= getDependencies((gate.in1, gate.in2), getIntermediates=getIntermediates)
    return dependencies
 
def getOutput(wires):     
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
    
    gatesToResolve = sorted([gate for gate in gates if gate[0] == "z"], key = lambda n: int(n[1:]))
    
    for gate in gatesToResolve:
        resolveGate(gate)
        
    number = 0
    for ind, name in enumerate(gatesToResolve):
        gate = gates[name]
        number += wires[gate.out] << ind
    return number
                    
if __name__ == "__main__":
    main()