#!/usr/bin/python3

import random

def random_key():
    l = [chr(random.randint(0, 255)) for i in range(16)]
    l = ''.join(l)
    return l.encode('latin')

key = random_key()
print(key)
print(len(key))
