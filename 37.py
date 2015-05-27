#!/usr/bin/python3

import random
from Crypto import Random 
from hashlib import sha1, sha256

def int_to_hash(num):
    return sha1(str(num).encode()).digest()[:16]

def hash_to_int(hash_str):
    res = 0
    exp = len(hash_str) - 1
    for a in hash_str:
        res += (2 ** (exp * 8)) * a
    return res

def get_session_key(self):
    s = pow(self.B, self.a, self.p)
    s = int_to_hash(s)
    return s

def random_integer():
    randbytes = Random.get_random_bytes(4)
    res = randbytes[0] * (2 ** 24) + randbytes[1] * (2 ** 16) + randbytes[2] * (2 ** 8) + randbytes[3]
    return res


def generate_salt():
    return random_integer()


class Network():
    def __init__(self):
        self.message = None
        
    def send(self, message):
        self.message = message

    def receive(self):
        res = self.message
        self.message = None
        return res
    

class Client():
    def __init__(self, N, g, k, I, P):
        self.N, self.g, self.k, self.I, self.P = N, g, k, I, P
        self.a = random.randint(0, self.N) % self.N
        self.A = pow(self.g, self.a, self.N)

    def receive_B(self, B):
        self.B = B
        uH = sha256((str(self.A) + str(self.B)).encode()).digest()
        u = hash_to_int(uH)
        self.u = u

    def receive_salt(self, salt):
        self.salt = salt
        xH = sha256((str(self.salt) + str(self.P)).encode()).digest()
        self.x = hash_to_int(xH)
        self.S = pow((self.B - self.k * pow(self.g, self.x, self.N)), self.a + self.u * self.x, self.N)
        self.S = 0              # we know it will be 0 on server side, so..
        self.K = sha256(str(self.S).encode()).digest()

class Server():
    def __init__(self, N, g, k, I, P):
        self.N, self.g, self.k, self.I, self.P = N, g, k, I, P
        self.salt = random_integer() 
        xH = sha256((str(self.salt) + self.P).encode()).digest()
        x = hash_to_int(xH)
        self.v = pow(self.g, x, self.N)
        self.b = random.randint(0, self.N) % self.N
        self.B = self.k * self.v + pow(self.g, self.b, self.N)

    def receive_A(self, A):
        self.A = A
        uH = sha256((str(self.A) + str(self.B)).encode()).digest()
        u = hash_to_int(uH)
        self.u = u
        self.S = pow(self.A * pow(self.v, self.u, self.N), self.b, self.N)
        self.K = sha256(str(self.S).encode()).digest()

def run():
    N = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
    g, k, I, P = 2, 3, 'ndarj11@freeuni.edu.ge', 'dzkonline.net'

    client = Client(N, g, k, I, None) # we don't know password
    server = Server(N, g, k, I, P)

    client.A = 0

    server.receive_A(client.A)
    client.receive_B(server.B)
    client.receive_salt(server.salt)

    if server.K == client.K:
        print("Accepted")
    else:
        print("Rejected")


if __name__ == '__main__':
    run()
