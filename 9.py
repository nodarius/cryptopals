#!/usr/bin/python3

def pad(text, blocksize):
    n = blocksize - len(text) % blocksize
    for i in range(0, n):
        text += chr(n).encode();
    return text

print(pad(b"YELLOW SUBMARINE", 20))
