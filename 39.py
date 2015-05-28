#!/usr/bin/python3

import random

def is_prime(num):
    for i in range(2, int(num / 2) + 1):
        if num % i == 0:
            return False
    return True
        
def generate_prime(low, high):
    for i in range(int(high / 2 - low / 2)):
        num = random.randint(low, high)
        if (is_prime(num)):
            return num
    return None

def invmod(x, N):
    for i in range(0, x):
        rem = (i * N + 1) % x
        if rem == 0:
            return (i * N + 1) / x
    return None

def run():
    p = generate_prime(1000, 20000)
    q = generate_prime(1000, 20000)
    n = p * q

    et = (p - 1) * (q - 1)
    e = 3
    inv = invmod(17, 3120)
    print(inv)
    print(p)
    print(q)
    print(n)
    print(et)



if __name__ == '__main__':
    run()
