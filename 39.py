#!/usr/bin/python3

import random
import base64

def is_prime(num):
    for i in range(2, int(num / 2) + 1):
        if num % i == 0:
            return False
    return True
        
def generate_prime(low, high):
#    print("generating prime")
    for i in range(int(high / 2 - low / 2)):
        num = random.randint(low, high)
        if (is_prime(num)):
#            print("Done")
            return num
    return None

from decimal import *
getcontext().prec = 100

def invmod(x, N):
    res = None
    for i in range(0, x):
        rem = (i * N + 1) % x
        if rem == 0:
            res = Decimal((i * N + 1) / Decimal(x))
            break

    if res != None and (x * res) % N != 1:
        print("invmod failed: x: %d, res: %d, n: %d" % (x, res, N))
        exit(0)

    return res


def encrypt(m, e, n):
    return pow(m, e, n)

def decrypt(c, d, n):
    return pow(c, d, n)

def run():
    p = q = n = et = e = None
    while True:
        p = generate_prime(1000000, 20000000)
        q = generate_prime(1000000, 20000000)
        n = p * q

        et = (p - 1) * (q - 1)
        e = 3
        d = invmod(e, et)
        if d != None:
            break
    public = e % n
    private = d % n
    secret = b'dzk'
    num = int(base64.b16encode(secret), 16)
#    print(num)
#    print(hex(num)[2:].upper())
#    print(base64.b16decode(hex(num)[2:].upper()))

    if num >= n:
        print("Too long string for our little primes")
        exit(0)
    c = encrypt(num, public, n)
    m = decrypt(c, private, n)
    m = int(m)
    m = hex(m)[2:].upper()
    plain = base64.b16decode(m)
    print(plain)



if __name__ == '__main__':
    run()
