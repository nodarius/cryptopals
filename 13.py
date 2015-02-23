#!/usr/bin/python3

import random
from Crypto.Cipher import AES

def pad(text, blocksize):
    n = blocksize - len(text) % blocksize
    for i in range(0, n):
        text += chr(n).encode();
    return text

def unpad(text):
    return text[:-text[len(text) - 1]]

def encrypt_ecb(key, string):
    return AES.new(key, AES.MODE_ECB, 'ignore').encrypt(pad(string, 16))

def decrypt_ecb(key, string):
    return unpad(AES.new(key, AES.MODE_ECB, 'ignore').decrypt(string))

def random_bytes(n):
    l = [chr(random.randint(0, 255)) for i in range(n)]
    l = ''.join(l)
    return l.encode('latin')



def parse(url):
    res = {}
    lst = url.split(b'&')
    for item in lst:
        key, val = item.split(b'=')
        res[key] = val
    return res


def profile_for(email):
    email = email.decode()
    if email.find('&') != -1 or email.find('=') != -1:
        print('error')
        return None
    return ('email=%s&uid=10&role=user' % email).encode()

key = random_bytes(16)
def encrypt_profile(encoded_profile):
    return encrypt_ecb(key, encoded_profile)

def decrypt_profile(encrypted_profile):
    return parse(decrypt_ecb(key, encrypted_profile))


def create_admin_profile():
    # if encoded profile has the length of 36, last 4 bytes will be 'user'
    # and since ecb encrypts 16 byte blocks, last block will be encryption
    # of 'user', so we delete that last block and change it with the encryption
    # of admin. that's whole algorithm.
    # the length of the email should be 13 for this.
    profile = profile_for(b'rap@yahoo.com')
    encrypted = encrypt_profile(profile)

    admin = pad(b'admin', 16)
    profile = profile_for(b'a' * 10 + admin + b'@yahoo.com')
    admin_encryption = encrypt_profile(profile)[16:32]
    encrypted = encrypted[:-16] + admin_encryption
    print(decrypt_profile(encrypted))

create_admin_profile()

