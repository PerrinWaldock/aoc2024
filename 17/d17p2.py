import numpy as np
from collections import deque
import re
import os
from tqdm import tqdm
import itertools
import sys

import dataclasses
from typing import Any

#note: this only works because the program iterates through A three digits at a time. Will not work for an arbitrary program

def main():
    filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input.txt")
    # filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample4.txt")

    with open(filename) as f:
        for line in f:
            if "Register A" in line:
                a = getIntsFromLine(line)[0]
            elif "Register B" in line:
                b = getIntsFromLine(line)[0]
            elif "Register C" in line:
                c = getIntsFromLine(line)[0]
            elif "Program" in line:
                program = list(getIntsFromLine(line))
        print(solveByDigits(program))
    
def getFirstOutputForA(program, a): 
    computer = Computer()
    num = computer.run(program, a=a, breakOnFirstOutput=True)
    return num

def getNextThreeDigits(program, expectedOutput, currentnumber):
    digits = format(currentnumber, 'b')
    numbersToTry = [int(digits+format(x, '03b'),2) for x in range(0,8)]
    validnumbers = [n for n in numbersToTry if expectedOutput == getFirstOutputForA(program, n)]
    return validnumbers

def solveByDigits(program, number=0, index=0):   
    if len(program) == index:
        #check that this number gives the correct output
        if not tryWithA(program, number):
            return None
        return number

    desired = program[len(program)-index-1]
    numbers = getNextThreeDigits(program, desired, number)
    for number in numbers:
        retval = solveByDigits(program, number, index+1)
        if retval is not None:
            return retval
    return None

def tryWithA(program,a):
    computer = Computer()
    output = computer.run(program,a)
    return output == program
    
def solveByBruteForce(program):
    a = 0
    with tqdm() as pbar:
        while not tryWithA(program, a):
            a += 1
            pbar.update(1)
    print(a)

def getIntsFromLine(line):
    return [int(n) for n in re.findall(r'-?\d+', line)]

class Computer:
    def __init__(self, a=0, b=0, c=0):
        self.a = a
        self.b = b
        self.c = c
        self.i = 0
        self.o = deque()
        
    def run(self, program, a=0, b=0, c=0, breakOnFirstOutput=False):
        self.a = a
        self.b = b
        self.c = c
        self.o = deque()
        self.i = 0
        while self.i < len(program) - 1:
            opcode = program[self.i]
            operand = program[self.i+1]
            #print(self.i, opcode, operand)
            self.compute(opcode, operand)
            self.i += 2
            if breakOnFirstOutput and len(self.o) > 0:
                return self.o[0]
        return list(self.o)
            
    
    def output(self, line):
        self.o.append(line)
    
    def getCombo(self, operand):
        if 0 <= operand <= 3:
            return operand
        elif 4 <= operand <= 6:
            if operand == 4:
                return self.a
            elif operand == 5:
                return self.b
            elif operand == 6:
                return self.c
        
    def compute(self, opcode, operand):
        if opcode == 0:
            self.a = self.a >> self.getCombo(operand)
        elif opcode == 1:
            self.b = self.b ^ operand
        elif opcode == 2:
            self.b = self.getCombo(operand % 8) % 8
        elif opcode == 3:
            if self.a != 0:
                self.i = operand - 2
        elif opcode == 4:
            self.b = self.b ^ self.c
        elif opcode == 5:
            self.output(self.getCombo(operand % 8) % 8)
        elif opcode == 6:
            self.b = self.a >> self.getCombo(operand)
        elif opcode == 7:
            self.c = self.a >> self.getCombo(operand)

if __name__ == "__main__":
    main()