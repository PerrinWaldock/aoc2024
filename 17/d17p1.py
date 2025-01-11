from collections import deque
import re
import os

def main():
    filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input.txt")
    # filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample.txt") #4,6,3,5,6,3,5,2,1,0
    # filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample2.txt") #0,1,2
    # filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample3.txt") # 4,2,5,6,7,7,7,7,3,1,0

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
    computer = Computer(a,b,c)
    computer.run(program)


def getIntsFromLine(line):
    return [int(n) for n in re.findall(r'-?\d+', line)]

class Computer:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        self.i = 0
        self.o = deque()
        
    def run(self, program):
        while self.i < len(program) - 1:
            opcode = program[self.i]
            operand = program[self.i+1]
            #print(self.i, opcode, operand)
            self.compute(opcode, operand)
            self.i += 2
        print(','.join([str(n) for n in self.o]))
            
    
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