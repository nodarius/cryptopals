#!/usr/bin/python3

from Crypto.Cipher import AES
import base64
import struct
import random

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


def random_bytes(n):
    l = [chr(random.randint(0, 255)) for i in range(n)]
    l = ''.join(l)
    return l.encode('latin')


base64_strings = [
    "SSBoYXZlIG1ldCB0aGVtIGF0IGNsb3NlIG9mIGRheQ==",
    "Q29taW5nIHdpdGggdml2aWQgZmFjZXM=",
    "RnJvbSBjb3VudGVyIG9yIGRlc2sgYW1vbmcgZ3JleQ==",
    "RWlnaHRlZW50aC1jZW50dXJ5IGhvdXNlcy4=",
    "SSBoYXZlIHBhc3NlZCB3aXRoIGEgbm9kIG9mIHRoZSBoZWFk",
    "T3IgcG9saXRlIG1lYW5pbmdsZXNzIHdvcmRzLA==",
    "T3IgaGF2ZSBsaW5nZXJlZCBhd2hpbGUgYW5kIHNhaWQ=",
    "UG9saXRlIG1lYW5pbmdsZXNzIHdvcmRzLA==",
    "QW5kIHRob3VnaHQgYmVmb3JlIEkgaGFkIGRvbmU=",
    "T2YgYSBtb2NraW5nIHRhbGUgb3IgYSBnaWJl",
    "VG8gcGxlYXNlIGEgY29tcGFuaW9u",
    "QXJvdW5kIHRoZSBmaXJlIGF0IHRoZSBjbHViLA==",
    "QmVpbmcgY2VydGFpbiB0aGF0IHRoZXkgYW5kIEk=",
    "QnV0IGxpdmVkIHdoZXJlIG1vdGxleSBpcyB3b3JuOg==",
    "QWxsIGNoYW5nZWQsIGNoYW5nZWQgdXR0ZXJseTo=",
    "QSB0ZXJyaWJsZSBiZWF1dHkgaXMgYm9ybi4=",
    "VGhhdCB3b21hbidzIGRheXMgd2VyZSBzcGVudA==",
    "SW4gaWdub3JhbnQgZ29vZCB3aWxsLA==",
    "SGVyIG5pZ2h0cyBpbiBhcmd1bWVudA==",
    "VW50aWwgaGVyIHZvaWNlIGdyZXcgc2hyaWxsLg==",
    "V2hhdCB2b2ljZSBtb3JlIHN3ZWV0IHRoYW4gaGVycw==",
    "V2hlbiB5b3VuZyBhbmQgYmVhdXRpZnVsLA==",
    "U2hlIHJvZGUgdG8gaGFycmllcnM/",
    "VGhpcyBtYW4gaGFkIGtlcHQgYSBzY2hvb2w=",
    "QW5kIHJvZGUgb3VyIHdpbmdlZCBob3JzZS4=",
    "VGhpcyBvdGhlciBoaXMgaGVscGVyIGFuZCBmcmllbmQ=",
    "V2FzIGNvbWluZyBpbnRvIGhpcyBmb3JjZTs=",
    "SGUgbWlnaHQgaGF2ZSB3b24gZmFtZSBpbiB0aGUgZW5kLA==",
    "U28gc2Vuc2l0aXZlIGhpcyBuYXR1cmUgc2VlbWVkLA==",
    "U28gZGFyaW5nIGFuZCBzd2VldCBoaXMgdGhvdWdodC4=",
    "VGhpcyBvdGhlciBtYW4gSSBoYWQgZHJlYW1lZA==",
    "QSBkcnVua2VuLCB2YWluLWdsb3Jpb3VzIGxvdXQu",
    "SGUgaGFkIGRvbmUgbW9zdCBiaXR0ZXIgd3Jvbmc=",
    "VG8gc29tZSB3aG8gYXJlIG5lYXIgbXkgaGVhcnQs",
    "WWV0IEkgbnVtYmVyIGhpbSBpbiB0aGUgc29uZzs=",
    "SGUsIHRvbywgaGFzIHJlc2lnbmVkIGhpcyBwYXJ0",
    "SW4gdGhlIGNhc3VhbCBjb21lZHk7",
    "SGUsIHRvbywgaGFzIGJlZW4gY2hhbmdlZCBpbiBoaXMgdHVybiw=",
    "VHJhbnNmb3JtZWQgdXR0ZXJseTo=",
    "QSB0ZXJyaWJsZSBiZWF1dHkgaXMgYm9ybi4="]


def encrypt_with_fixed_nonce(base64lst, nonce, key):
    res = []
    for b64 in base64lst:
        plain = base64.b64decode(b64)
        enc = encrypt_ctr(key, plain, nonce)
        res.append(enc)
    return res

    
def print_single_byte_xors(encs, guessed_keystream):
    maxlen = len(max(encs, key=len))
    for i in range(maxlen):
        print("Printing single byte xor, byte index - %d:" % i)
        for enc in encs:
            if len(enc) > i:
                #print(chr(enc[i]), end='')
                pass
        print("")
        for enc in encs:
            if len(enc) > i:
                plain = chr((guessed_keystream[i] ^ enc[i]))
                print(plain, end='')
        print("")
        for enc in encs:
            if len(enc) > i:
                plain = guessed_keystream[i] ^ enc[i]
                print("%d|" % plain, end='')
        print("")
        for enc in encs:
            if len(enc) > i:
                print("%d|" % enc[i], end='')

        print("")
        print("-" * 80)

def print_xors(encs, key):
    for enc in encs:
        res = xor_encrypt(enc, key);
        print(res)



# According to the description, must be done with thinking and substituting
# piecemal. Without automation. So, the code only prints the result,
# not including the steps of how I get to it.
def main():
    key = base64.b64decode("/n7dJrVnFuRFdKeZvihsAg==")
    nonce = 0
    encs = encrypt_with_fixed_nonce(base64_strings, nonce, key)
    guessed_keystream = b'\xb2\x07\x40\x34\xed\x3e\x0c\x3f\x59\xff\x69\xc2\x63\x19\x1a\x7d\x95\xcf\xcd\x51\xd1\x92\xe6\x56\x79\xf0\x14\x4c\x66\x34\xe7\x09\x4d\x56\x43\x41\x27\xaa\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0'
    # print_single_byte_xors(encs, guessed_keystream)
    print_xors(encs, guessed_keystream);

main()
    
