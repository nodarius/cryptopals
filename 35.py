#!/usr/bin/python3

import random
from Crypto import Random as crandom
from Crypto.Cipher import AES
from hashlib import sha1

def pad(text, blocksize):
    n = blocksize - len(text) % blocksize
    for i in range(0, n):
        text += chr(n).encode();
    return text

def unpad(string):
    size = string[-1]
    return string[:-size]

def int_to_hash(num):
    return sha1(str(num).encode()).digest()[:16]

class A:
    def __init__(self):
        self.p = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
        self.g = 2
        self.a = random.randint(0, self.p) % self.p
        self.A = pow(self.g, self.a, self.p)

    def get_A(self):
        return self.A

    def set_B(self, B):
        self.B = B

    def get_p(self):
        return self.p

    def get_g(self):
        return self.g

    def get_session_key(self):
        s = pow(self.B, self.a, self.p)
        s = int_to_hash(s)
        return s

    def get_message(self):
        self.message = b'All hail Totti'
        key = self.get_session_key()
        iv = crandom.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        enc = cipher.encrypt(pad(self.message, AES.block_size)) + iv
        return enc

class B:
    def __init__(self):
        pass

    def set_p(self, p):
        self.p = p
        self.b = random.randint(0, self.p) % self.p

    def set_g(self, g):
        self.g = g

    def set_A(self, A):
        self.A = A

    def get_B(self):
        self.B = pow(self.g, self.b, self.p)
        return self.B

    def get_session_key(self):
        s = pow(self.A, self.b, self.p)
        s = int_to_hash(s)
        return s

    def receive_message(self, message):
        key = self.get_session_key()
        iv = message[-16:]
        message = message[:-16]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        dec = unpad(cipher.decrypt(message))
        self.message = dec

    def get_message(self):
        return self.message


def run_mitm_1():
    print("Running MITM with g=1..", end=' ')
    a, b = A(), B()
    b.set_p(a.get_p())
    b.set_g(1)
#    b.set_g(a.get_g())
    b.set_A(a.get_A())
    a.set_B(b.get_B())
    
    msg_a = a.get_message()
    key = int_to_hash(1)
    iv = msg_a[-16:]
    msg_a = msg_a[:-16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    dec = unpad(cipher.decrypt(msg_a))
    print("Decripted: %s" % dec)

def run_mitm_2():

    pass
def run_mitm_3():
    pass



def run_normal():
    print("Running normal..", end=' ')
    a, b = A(), B()
    b.set_p(a.get_p())
    b.set_g(a.get_g())
    b.set_A(a.get_A())
    a.set_B(b.get_B())
    
    session = None
    if b.get_session_key() == a.get_session_key():
        session = int_to_hash(a.get_session_key())
    b.receive_message(a.get_message())
    print("Done.")

if __name__ == '__main__':
    run_normal()
    run_mitm_1()
    run_mitm_2()
    run_mitm_3()
