#!/usr/bin/python3

from Crypto.Cipher import AES
import random
import math
import base64

def pad(text, blocksize):
    n = blocksize - len(text) % blocksize
    for i in range(0, n):
        text += chr(n).encode();
    return text

class IncorrectPadding(Exception):
    pass

def unpad_exc(string):
    size = string[-1]
    if size == 0 or size >= len(string):
        raise IncorrectPadding

    for i in range(1, size + 1):
        if string[-size] != size:
            raise IncorrectPadding
    return string[:-size]

def xor_encrypt(str, key):
    full_key = b''
    while(len(full_key) < len(str)):
        full_key += key
    l = [chr(a ^ b) for a, b in zip(str, full_key)]
    return ''.join(l).encode('latin')

def encrypt_ecb(key, string):
    return AES.new(key, AES.MODE_ECB, 'ignore').encrypt(string)

def decrypt_ecb(key, string):
    return AES.new(key, AES.MODE_ECB, 'ignore').decrypt(string)

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

def decrypt_cbc(key, string, iv):
    blocksize = 16
    res = b''
    prev = iv
    for i in range(0, len(string), blocksize):
        block = string[i:i + blocksize]
        decrypted_block = decrypt_ecb(key, block)
        plain = xor_encrypt(decrypted_block, prev)
        prev = block
        res += plain
    return unpad_exc(res)


def random_bytes(n):
    l = [chr(random.randint(0, 255)) for i in range(n)]
    l = ''.join(l)
    return l.encode('latin')

enc_lst = ['MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=', 'MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=', 'MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==', 'MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==', 'MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl', 'MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==', 'MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==', 'MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=', 'MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=', 'MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93']

key = random_bytes(16)
iv = random_bytes(16)

def encrypt():
    plain = enc_lst[random.randint(0, len(enc_lst) - 1)]
    plain = base64.b64decode(plain)
    enc = encrypt_cbc(key, plain, iv)
    return enc, iv

def has_correct_padding(enc, iv):
    try:
        decrypt_cbc(key, enc, iv)
    except IncorrectPadding:
        return False
    else:
        return True

def decrypt_block(block, iv):
    res = b''
    original_iv = iv[:]

    for ind in range(1, 17):
        for ch in range(0, 256):
            iv = iv[:16 - ind] + (chr(ch)).encode('latin') + iv[16 - ind + 1:]
            if has_correct_padding(block, iv):
                x = ch ^ ind
                res = chr(original_iv[-ind] ^ x).encode() + res
                print(str(ind) + ' ' + chr(ch) + ' ' + chr(original_iv[-ind] ^ x))
                for i in range(1, ind + 1):
                    lst_iv = list(iv)
                    lst_iv[-i] = lst_iv[-i] ^ ind ^ (ind + 1)
                    iv = b''.join([chr(a).encode('latin') for a in lst_iv])
                break
    print(res)
    return b'a' * 16

def decrypt():
    enc, iv = encrypt()
    decrypted = b''
    prev = iv
    return decrypt_block(enc[0:16], iv)

    for i in range(0, len(enc), 16):
        block = enc[i:i + 16]
        prev = decrypt_block(block, prev)
        decrypted += prev
    return decrypted

print(decrypt())
