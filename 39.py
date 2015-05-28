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


def run():
    prime = generate_prime(1000, 20000)
    print(prime)


if __name__ == '__main__':
    run()
