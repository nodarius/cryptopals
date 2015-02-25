#!/usr/bin/python3

class IncorrectPadding(Exception):
    pass

def pad(text, size):
    diff = size - len(text) % size
    for i in range(diff):
#        print(chr(diff).encode())
        text += chr(diff).encode()
    return text


def unpad_exc(string):
    size = string[-1]
    if size == 0 or size >= len(string):
        raise IncorrectPadding

    for i in range(1, size + 1):
        if string[-size] != size:
            raise IncorrectPadding
    return string[:-size]

