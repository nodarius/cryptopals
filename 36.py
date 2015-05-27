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
    def __init__(self):
        pass

class Server():
    def __init__(self):
        pass

def run():
    client, server = Client(), Server()

    client.N = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
    server.N = client.N
    client.g, server.g = 2, 2
    client.k, server.k = 3, 3
    client.I = 'ndarj11@freeuni.edu.ge'
    server.I = client.I
    client.P = 'dzkonline.net'
    server.P = client.P

    server.salt = random_integer() 
    xH = sha256((str(server.salt) + server.P).encode()).digest()
    x = hash_to_int(xH)
    server.v = pow(server.g, x, server.N)

    client.a = random.randint(0, client.N) % client.N
    client.A = pow(client.g, client.a, client.N)
    server.A = client.A

    server.b = random.randint(0, server.N) % server.N
    server.B = server.k * server.v + pow(server.g, server.b, server.N)
    client.B = server.B
    client.salt = server.salt
    uH = sha256((str(server.A) + str(server.B)).encode()).digest()
    u = hash_to_int(uH)
    server.u = u
    client.u = u
    xH = sha256((str(client.salt) + str(client.P)).encode()).digest()
    client.x = hash_to_int(xH)
    client.S = pow((client.B - client.k * pow(client.g, client.x, client.N)), client.a + client.u * client.x, client.N)
    client.K = sha256(str(client.S).encode()).digest()

    server.S = pow(server.A * pow(server.v, server.u, server.N), server.b, server.N)
    server.K = sha256(str(server.S).encode()).digest()

    if server.K == client.K:
        print("Accepted")
    else:
        print("Rejected")


if __name__ == '__main__':
    run()
