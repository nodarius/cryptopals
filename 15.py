#!/usr/bin/python3

class IncorrectPadding(Exception):
    pass

def unpad_exc(string):
    size = string[-1]
    if size == 0 or size > len(string):
        raise IncorrectPadding

    for i in range(1, size + 1):
        if string[-i] != size:
            raise IncorrectPadding
    return string[:-size]

