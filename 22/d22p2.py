import numpy as np
from collections import deque
import os
from tqdm import tqdm


def main():
    filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input.txt")
    #filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample.txt")
    #filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sample2.txt")
    
    seeds = deque()
    with open(filename) as f: 
        for line in f:
            seeds.append(int(line))  
            
    lookups = deque()
    for seed in seeds:
        lookups.append(getPricesLookup(seed, 2000, 4))
    sequences = set()
    for lookup in lookups:
        sequences |= set(lookup)
    
    bestScore = 0
    for sequence in tqdm(sequences):
        score = getProfitFromSequence(sequence, lookups)
        if score > bestScore:
            bestScore = score
    print(bestScore)

def mix(secret, number):
    return number ^ secret

def prune(secret):
    return secret & 0xFFFFFF # %16777216 #this is 2^24 so can calculate by anding with 0xFFFFFF

def generateNextNumber(secret):
    nextNumber = secret << 6
    secret = mix(secret, nextNumber)
    secret = prune(secret)
    
    nextNumber = secret >> 5
    secret = mix(secret, nextNumber)
    secret = prune(secret)
    
    nextNumber = secret << 11 #TODO bitshift
    secret = mix(secret, nextNumber)
    secret = prune(secret)
    
    return secret

def getPrices(seed, n):
    numbers = deque()
    numbers.append(seed % 10)
    for _ in range(n):
        seed = generateNextNumber(seed)
        numbers.append(seed % 10)
    return list(numbers)

def getPricesLookup(seed, n, m):
    prices = getPrices(seed, n)
    diff = getChanges(prices)
    
    lookup = dict()
    for i in range(len(diff) - m):
        key = tuple(diff[i:i + m])
        if not key in lookup:
            lookup[key] = prices[i+m]
    return lookup

def getChanges(prices):
    return list(np.diff(prices))

def findFirstOccurence(sequence, pattern=[]):
    found = False
    pattern = list(pattern)
    for i in range(len(sequence) - len(pattern)):
        if sequence[i:i + len(pattern)] == pattern:
            found = True
            break
    if found:
        return i

def findSequencesOfLength(sequence, n):
    sequences = set()
    for i in range(len(sequence) - n):
        sequences.add(tuple(sequence[i:i + n]))
    return sequences

def findAllSequencesOfLength(sequences, n):
    seqSet = set()
    for sequence in sequences:
        seqSet |= findSequencesOfLength(sequence, n)
    return seqSet

def getSaleForSequence(sequence, prices, diff):
    index = findFirstOccurence(diff, sequence)
    if index is None:
        return 0
    else:
        return prices[index + len(sequence) - 1]
    
def getProfitFromSequence(sequence, lookups):
    total = 0
    for lookup in lookups:
        if sequence in lookup:
            total += lookup[sequence]
    return total

if __name__ == "__main__":
    main()