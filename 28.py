#!/usr/bin/python3


def sha1(message):
    pass
#    h0 = 0x67452301
#    h1 = 0xEFCDAB89
#    h2 = 0x98BADCFE
#    h3 = 0x10325476
#    h4 = 0xC3D2E1F0

#    ml = len(message) * 8       # message length in bits
#    message += b'\x80'
    

    return b''


import base64
def test():
    res = sha1(b'eminem')
    res = base64.b16encode(res)
    if res != b'5254792d5579984f98c41d1858e1722b2dbcc6b3':
        print("Error")
    else:
        print("Success")


test()
