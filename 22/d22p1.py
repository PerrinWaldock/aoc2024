from collections import deque
import os


def main():
    filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input.txt")
    # filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample.txt")
    
    seeds = deque()
    with open(filename) as f:
        for line in f:
            seeds.append(int(line))   
            
    sum = 0
    for seed in seeds:
        sum += getNthNumber(seed, 2000)
    print(sum)

def mix(secret, number):
    return number ^ secret

def prune(secret):
    return secret%16777216 #this is 2^24 so can calculate by anding with 0xFFFFFF

def generateNextNumber(secret):
    nextNumber = secret*64 #TODO bitshift
    secret = mix(secret, nextNumber)
    secret = prune(secret)
    
    nextNumber = secret//32 #TODO bitshift
    secret = mix(secret, nextNumber)
    secret = prune(secret)
    
    nextNumber = secret*2048 #TODO bitshift
    secret = mix(secret, nextNumber)
    secret = prune(secret)
    
    return secret

def getNthNumber(seed, n):
    for _ in range(n):
        seed = generateNextNumber(seed)
    return seed
    

if __name__ == "__main__":
    main()