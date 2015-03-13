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



import time
def timestamp():
    return int(time.time())

def generate_random_bit():
    num = extract_number() % 256
    return num #chr(num).encode('latin')

def mt19937_encrypt(seed, plain):
    initialize_generator(seed)
    res = b''
    for i in range(0, len(plain)):
        res += chr(generate_random_bit() ^ plain[i]).encode('latin')
    return res

def num_to_bin(num):
    return "{0:b}".format(num)

import random

def random_bytes(n):
    l = [chr(random.randint(0, 255)) for i in range(n)]
    l = ''.join(l)
    return l.encode('latin')


def truncate(num, nbits):
    return int(num_to_bin(num)[0:nbits], 2)
    
def encrypt_with_random_prefix(plain):
    seed = truncate(timestamp(), 16)
    prefix = random_bytes(random.randint(100, 1000))
    enc = mt19937_encrypt(seed, prefix + plain)
    return enc

def recover_the_key(enc, known_sufix):
    pref_len = len(enc) - len(known_sufix)
    pref = b'a' * pref_len
    print("Iterating from %d to %d" % (2 ** 15, 2 ** 16 + 1))
    for i in range(2 ** 15, 2 ** 16 + 1):
        seed = i
        if i % 1000 == 0:
            print(i)
        dec = mt19937_encrypt(seed, enc)
        if dec[-len(known_sufix):] == known_sufix:
            print("seed is: %d" % i)
            return i
    print("Couldn't recover key")
    return None

def main():
    plain = b'A' * 14
    enc = encrypt_with_random_prefix(plain)
    recovered_seed = recover_the_key(enc, plain)
    if recovered_seed is not None:
        print("Recovered seed: %d " % recovered_seed)
    

main()

"""
remaining:

>>> Use the same idea to generate a random "password reset token" using MT19937 seeded from the current time.
>>> Write a function to check if any given password token is actually the product of an MT19937 PRNG seeded with the current time.

^^^
Couldn't understand what you are asking exactly... should thinkg again after some time

"""
