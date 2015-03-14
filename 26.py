#!/usr/bin/python3

from Crypto.Cipher import AES
import random
import math

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


import struct
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
def random_bytes(n):
    l = [chr(random.randint(0, 255)) for i in range(n)]
    l = ''.join(l)
    return l.encode('latin')

prepend = b'comment1=cooking%20MCs;userdata='
append = b';comment2=%20like%20a%20pound%20of%20bacon'
key = random_bytes(16)
iv = random_bytes(16)

def first(user_str):
    if user_str.find(b';') != -1 or user_str.find(b'=') != -1:
        return None
    plain = prepend + user_str + append
    return encrypt_ctr(key, plain, 0)

admintoken = b';admin=true;'

def second(encrypted):
    plain = decrypt_ctr(key, encrypted, 0)
    print(plain)
    if plain.find(admintoken) != -1:
        return True
    return False

def become_admin():
    food = b'a' * len(admintoken)
    enc = first(food)
    key = xor_encrypt(enc[len(prepend):len(prepend) + len(food)], food)
    food = xor_encrypt(key, admintoken)
    enc = enc[:len(prepend)] + food + enc[len(prepend) + len(food):]

    if(second(enc)):
        print("Hello Admin")
    else:
        print("You are not admin... get lost")

become_admin()

