#!/usr/bin/python3

import random

def dh():
    p = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
    g = 2

    a = random.randint(0, p) % p
    A = pow(g, a, p)
    b = random.randint(0, p) % p
    B = pow(g, b, p)

    s = pow(B, a, p)
    s1 = pow(A, b, p)
    if s1 != s:
        print("error")
    else:
        print("ok")
    return s

from hashlib import sha1
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

    def send2(self):
        #hsh = sha1.digest(str(self.s).encode()).digest()
        pass
    def get_session_key(self):
        s = pow(self.B, self.a, self.p)
        return s

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
        return s

class M:
    def __init__(self):
        pass


def run():
    a, b = A(), B()
    b.set_A(a.get_A())
    b.set_p(a.get_p())
    b.set_g(a.get_g())
    a.set_B(b.get_B())
    s = b.get_session_key()
    print(s)
    s1 = a.get_session_key()
    print(s1)
    if s1 == s:
        print('ok')

if __name__ == '__main__':
    run()
