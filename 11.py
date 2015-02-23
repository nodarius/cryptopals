#!/usr/bin/python3

import random
from Crypto.Cipher import AES

def pad(text, blocksize):
    n = blocksize - len(text) % blocksize
    for i in range(0, n):
        text += chr(n).encode();
    return text

def xor_encrypt(str, key):
    full_key = b''
    while(len(full_key) < len(str)):
        full_key += key
    l = [chr(a ^ b) for a, b in zip(str, full_key)]
    return ''.join(l).encode('latin')

def encrypt_ecb(key, string):
    return AES.new(key, AES.MODE_ECB, 'ignore').encrypt(pad(string, 16))

def encrypt_cbc(key, string, iv):
    blocksize = 16
    string = pad(string, blocksize)
    prev = iv
    res = b''
    for i in range(0, len(string), blocksize):
        block = string[i:i + blocksize]
        xoredblock = xor_encrypt(block, prev)
        encrypted_block = encrypt_ecb(key, xoredblock)
        prev = encrypted_block
        res += encrypted_block
    return res


def random_bytes(n):
    l = [chr(random.randint(0, 255)) for i in range(n)]
    l = ''.join(l)
    return l.encode('latin')

def magic_encrypt(plain):
    key = random_bytes(16)
    before = random_bytes(random.randint(5, 10))
    after = random_bytes(random.randint(5, 10))
    plain = before + plain + after
    if random.getrandbits(1):
        iv = random_bytes(16)
        return encrypt_cbc(key, plain, iv), "cbc"
    else:
        return encrypt_ecb(key, plain), "ecb"

def detect_algorithm():
    plain = b'a' * 1280
    encrypted, algorithm = magic_encrypt(plain)
    res = "cbc"
    for i in range(0, int((len(encrypted) - 32) / 16), 16):
        if encrypted[i:i + 16] == encrypted[i + 16:i + 32]:
            res = 'ecb'
            break
    if res != algorithm:
        return False
    else:
        return True

def check():
    err = 0
    success = 0
    for i in range(0, 100):
        if (detect_algorithm()):
            success += 1
        else:
            err += 1
    print("%d errors, %d success" % (err, success))
check()
