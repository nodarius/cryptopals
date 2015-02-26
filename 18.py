#!/usr/bin/python3

from Crypto.Cipher import AES
import base64
import struct

def encrypt_ecb(key, string):
    return AES.new(key, AES.MODE_ECB, 'ignore').encrypt(string)

def decrypt_ecb(key, string):
    return AES.new(key, AES.MODE_ECB, 'ignore').decrypt(string)

def xor_encrypt(str, key):
    full_key = b''
    while(len(full_key) < len(str)):
        full_key += key
    l = [chr(a ^ b) for a, b in zip(str, full_key)]
    return ''.join(l).encode('latin')


def bits(i):
    return struct.pack('L', i)

def encrypt_ctr(key, text, nonce):
    nonce = bits(nonce)
    n = int(len(text) / 16) + 1
    encrypted = b''
    for i in range(0, n):
        block = nonce + bits(i)
        encrypted += encrypt_ecb(key, block)
    res = xor_encrypt(text, encrypted)
    return res

def decrypt_ctr(key, text, nonce):
    return encrypt_ctr(key, text, nonce)
    return b''

str64 = b'L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=='
key = b'YELLOW SUBMARINE'
nonce = 0

def check():
    dec = decrypt_ctr(key, base64.b64decode(str64), nonce)
    print('Decripted: %s' % dec)
    test = b'nodarius_' * 19
    print('now encrypting some test string')
    enc = encrypt_ctr(key, test, nonce)
    print('Done. now decrypting.')
    dec = decrypt_ctr(key, enc, nonce)
    if dec == test:
        print("Decrypted successfully!")
    else:
        print("Error")

check()
    
