#!/usr/bin/python3

# Mersenne twister random number generator, implemented
# according to pseudo code at:
# http://en.wikipedia.org/wiki/Mersenne_twister#Pseudocode

MT = [0 for a in range(624)]
index = 0

import struct
def bits(i):
    return struct.pack('L', i)

def num_to_bin(num):
    return "{0:b}".format(num)

def initialize_generator(seed):
    global index
    index = 0
    MT[0] = seed
    for i in range(1, 624):
        a = 1812433253 * (MT[i - 1] ^ (MT[i - 1] >> 30) + 1)
        a = str(num_to_bin(a))[-32:] # get lowest 32 bits
        a = int(a, 2)
        MT[i] = a

def generate_numbers():
    for i in range(0, 624):
        y = (MT[i] & 0x80000000) + (MT[(i + 1) % 624] & 0x7fffffff)
        MT[i] = MT[(i + 397) % 624] ^ (y >> 1)
        if y % 2 is not 0:
            MT[i] = MT[i] ^ 2567483615


def extract_number():
    global index
    if index is 0:
        generate_numbers()

    y = MT[index]
    y = y ^ (y >> 1)
    y = y ^ ((y << 7) & 2636928640)
    y = y ^ ((y << 15) & 4022730752)
    y = y ^ (y >> 18)
    index = (index + 1) % 624
    return y

initialize_generator(10)
print(extract_number())
