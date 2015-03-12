#!/usr/bin/python3

# Mersenne twister random number generator, implemented
# according to pseudo code at:
# http://en.wikipedia.org/wiki/Mersenne_twister#Pseudocode

MT = [0 for a in range(624)]
index = 0

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

import random
import time
def timestamp():
    return int(time.time())

def invert_left(y, nshift, num):
    print(num_to_bin(y))
    pass

def test_left_invert():
#    print("Testing left invert.. ", end='', flush=True)
    y = random.randint(0, 10000000000000)
    y1 = y ^ ((y << 7) & 2636928640)
    print(num_to_bin(y))
    print(num_to_bin(y << 7))
    print(num_to_bin((y << 7) & 2636928640))
    print(num_to_bin(y1))
    exit()
    y2 = invert_left(y1, 7, 2636928640)
    if y != y2:
        print("Error")
    else:
        print("Success")


def invert_right(y, nshift):
    binary = num_to_bin(y)
    length = len(binary)
    nshift = length - nshift if length >= nshift else 0
    origin = num_to_bin(y >> (nshift))
    origin = str(origin).encode('latin')
    i = 0
    pref_len = len(origin)
    while len(origin) < length:
        origin = origin + chr(origin[i] ^ int(binary[pref_len + i])).encode()
        i += 1

    return int(origin.decode(), 2)




def test_right_invert():
    print("Testing right invert.. ", end='', flush=True)
    y = random.randint(0, 10)
    y1 = y ^ (y >> 18)
    y2 = invert_right(y1, 18)
    if y != y2:
        print("Error")
    else:
        print("Success")


def untemper(y):
    test_right_invert()
    test_left_invert()
    pass


def main():
    initialize_generator(timestamp())
    untemper(extract_number())
main()
