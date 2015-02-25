#!/usr/bin/python3

import random
from Crypto.Cipher import AES
import base64

def pad(text, blocksize):
    n = blocksize - len(text) % blocksize
    for i in range(0, n):
        text += chr(n).encode();
    return text

def unpad(text):
    return text[:-text[len(text) - 1]]


def encrypt_ecb(key, string):
    return AES.new(key, AES.MODE_ECB, 'ignore').encrypt(pad(string, 16))

def random_bytes(n):
    l = [chr(random.randint(0, 255)) for i in range(n)]
    return ''.join(l).encode('latin')


key = random_bytes(16)
random_str = random_bytes(random.randint(10, 100))

def oracle(plain):
    secret = """Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"""
    plain = random_str + plain + base64.b64decode(secret)
    return encrypt_ecb(key, plain)
    
def detect_blocksize():
    length = len(oracle(b'a'))
    for i in range(0, 256):
        enc = oracle(b'a' * i)
        diff = len(enc) - length
        if (diff > 0):
            return diff
    return None

def detect_algorithm(blocksize):
    plain = b'a' * 1280
    encrypted = oracle(plain)
    res = "cbc"
    for i in range(0, len(encrypted) - blocksize * 2, blocksize):
        if encrypted[i:i + blocksize] == \
           encrypted[i + blocksize:i + 2 * blocksize]:
            res = 'ecb'
            break
    return res

import math

def decrypt_with_known_randsize(randsize, blocksize):
    extra_foodlen = math.ceil(randsize / blocksize) * blocksize - randsize
    extra_len = math.ceil(randsize / blocksize) * blocksize
    foodlen = extra_foodlen + blocksize - 1
    food = b'a' * foodlen
    decrypted = b''
    size = 0
    while True:
        enc = oracle(food)
        start = len(decrypted) - len(decrypted) % blocksize + extra_len
        end = start + blocksize
        if size == len(enc):
            return unpad(decrypted)
        for i in range(0, 256):
            test_block = food + decrypted \
                         + chr(i).encode('latin')
            test_enc = oracle(test_block)
            if test_enc[start:end] == enc[start:end]:
                decrypted += chr(i).encode()
                food = b'a' * (blocksize - len(decrypted) % blocksize - 1 + \
                               extra_foodlen)
                break
        size += 1

def detect_minimum_rand_size(blocksize):
    a = oracle(b'a')
    b = oracle(b'b')
    size = 0
    for i in range(0, len(a)):
        if a[i] != b[i]:
            break
        size += 1
    return size - size % blocksize
    

def decrypt():
    blocksize = detect_blocksize()
    algorithm = detect_algorithm(blocksize)
    if algorithm != 'ecb':
        return

    size = detect_minimum_rand_size(blocksize)
    while True:
        print('assuming random length is: %d... ' % size, end = '')
        res = decrypt_with_known_randsize(size, blocksize)
        if res:
            print('Success.')
            return res
        print('Failed.')
        size += 1



print(decrypt())




