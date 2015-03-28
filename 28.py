#!/usr/bin/python3
"""
Mostly copied from https://github.com/ajalt/python-sha1/blob/master/sha1.py
as the description said: Find a SHA-1 implementation in the language you code in.
"""

import struct

def left_rotate(n, b):
    return ((n << b) | (n >> (32 - b))) & 0xffffffff

def sha1(message):
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0

    ml = len(message) * 8       # message length in bits
    message += b'\x80'
    while (len(message) * 8) % 512 != 448:
        message += b'\x00'
    message += struct.pack(b'>Q', ml)
    for i in range(0, len(message), 64):
        w = [0] * 80
        for j in range(16):
            w[j] = struct.unpack(b'>I', message[i + j*4:i + j*4 + 4])[0]
        for j in range(16, 80):
            w[j] = left_rotate(w[j-3] ^ w[j-8] ^ w[j-14] ^ w[j-16], 1)
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4        

        for j in range(80):
            if 0 <= j <= 19:
                # Use alternative 1 for f from FIPS PB 180-1 to avoid ~
                f = d ^ (b & (c ^ d))
                k = 0x5A827999
            elif 20 <= j <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= j <= 59:
                f = (b & c) | (b & d) | (c & d) 
                k = 0x8F1BBCDC
            elif 60 <= j <= 79:
                f = b ^ c ^ d
                k = 0xCA62C1D6
    
            a, b, c, d, e = ((left_rotate(a, 5) + f + e + k + w[j]) & 0xffffffff, 
                            a, left_rotate(b, 30), c, d)

        h0 = (h0 + a) & 0xffffffff
        h1 = (h1 + b) & 0xffffffff 
        h2 = (h2 + c) & 0xffffffff
        h3 = (h3 + d) & 0xffffffff
        h4 = (h4 + e) & 0xffffffff

    return ('%08x%08x%08x%08x%08x' % (h0, h1, h2, h3, h4)).encode()


def test():
    res = sha1(b'eminem')
    if res != b'5254792d5579984f98c41d1858e1722b2dbcc6b3':
        print("Error")
    else:
        print("Success")

def sha1_auth(message):
    secret = b'nodarius'
    return sha1(secret + message)

if __name__ == '__main__':
    test()
    print(sha1_auth(b"Eminem"))
