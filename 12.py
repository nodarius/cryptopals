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

def oracle(plain):
    secret = """Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"""
    plain = plain + base64.b64decode(secret)
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


def decrypt_block(index, prev_plain, blocksize):
    food = b'a' * (blocksize - 1)
    if prev_plain == None:
        prev_plain = food
    else:
        prev_plain = prev_plain[1:]

    decrypted = b''
    start = index * blocksize
    end = start + blocksize
    for i in range(0, blocksize):
        enc = oracle(food)
        for i in range(0, 256):
            test_block = prev_plain + chr(i).encode('latin')
            test_enc = oracle(test_block)
            if test_enc[:blocksize] == enc[start:end]:
                decrypted += chr(i).encode()
                food = food[1:]
                prev_plain = prev_plain[1:] + chr(i).encode()
                break
    return decrypted

def test(blocksize):
    food = b'a' * (blocksize - 1)
    decrypted = b''
    size = 0
    while True:
        enc = oracle(food)
        start = len(decrypted) - len(decrypted) % blocksize
        end = start + blocksize
        for i in range(0, 256):
            test_block = food + decrypted[-blocksize + 1:] \
                         + chr(i).encode('latin')
            test_enc = oracle(test_block)
            if i == 0:
               print("test block is %s" % test_block)            
            if test_enc[:blocksize] == enc[start:end]:
                decrypted += chr(i).encode()
                food = b'a' * (blocksize - len(decrypted) % blocksize - 1)
                print(chr(i))
                break

        size += 1



    
print(test(detect_blocksize()))

def decrypt():
    blocksize = detect_blocksize()
    algorithm = detect_algorithm(blocksize)
    if algorithm != 'ecb':
        return

    res = b''
    block = None
    i = 0
    while True:
        block = decrypt_block(i, block, blocksize)
        i += 1
        res += block
        if not block:
            break

    return unpad(res)



print(decrypt())

