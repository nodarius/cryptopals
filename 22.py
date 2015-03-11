#!/usr/bin/python3

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

def wait_random_seconds(low, high):
    time.sleep(random.randint(low, high))

def timestamp():
    return int(time.time())
    
def truncate_number(num, size):
    num = str(num_to_bin(num))[:size] 
    num = int(num, 2)
    return num
    

def get_magic_random_number():
    wait_random_seconds(40, 1000)
    initialize_generator(timestamp())
    wait_random_seconds(40, 1000)
    rand = extract_number()
    rand = truncate_number(rand, 32)
    return rand


def extract_seed():
    start_time = timestamp()
    print("start time is: %d", start_time)
    rand = get_magic_random_number()
    end_time = timestamp()
    print("end time is: %d", end_time)
    found = False
    for i in range(start_time, end_time + 1):
        initialize_generator(i)
        num = extract_number()
        num = truncate_number(num, 32)
        if num == rand:
            print("Seed was: %d", i)
            found = True
            break
    if not found:
        print("Could not extract seed.")

extract_seed()    
