#!/usr/bin/python3

from Crypto.Cipher import AES
import random

def pad(text, blocksize):
    n = blocksize - len(text) % blocksize
    for i in range(0, n):
        text += chr(n).encode();
    return text

class IncorrectPadding(Exception):
    pass

def unpad_exc(string):
    size = string[-1]
    if size == 0 or size > len(string):
        raise IncorrectPadding

    for i in range(1, size + 1):
        if string[-i] != size:
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

def is_ascii(string):
    for a in string:
        if a >= 128:
            return False
    return True
        

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

prepend = b'comment1=cooking%20MCs;userdata='
append = b';comment2=%20like%20a%20pound%20of%20bacon'
key = random_bytes(16)
iv = key

def first(user_str):
    if user_str.find(b';') != -1 or user_str.find(b'=') != -1:
        return None
    plain = prepend + user_str + append
    plain = user_str
    return encrypt_cbc(key, plain, iv)

def second(encrypted):
    plain = b''
    plain = decrypt_cbc(key, encrypted, iv)
    if is_ascii(plain):
        return None
    else:
        return plain



def main():
    blocksize = 16
    enc = first(b'a' * blocksize * 3)
    food = enc[:blocksize] + b'\0' * blocksize + enc[:blocksize] + enc[blocksize:]
    dec = second(food)
    extracted_key = xor_encrypt(dec[:blocksize], dec[2 * blocksize:3 * blocksize])
    if extracted_key == key:
        print('Done! you have extracted key successfully')
    else:
        print("You couldn't extract the key..")

main()
