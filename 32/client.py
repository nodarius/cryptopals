#!/usr/bin/python3

import http.client
from timeit import default_timer as timer

def generate_url(filename, mac):
    return '/?file=' + filename + '&mac=' + mac

alphabet = '0123456789abcdef'
#b'e05fd606b6ff172edba27e0789bdfb9f'
def run(filename):
    h1 = http.client.HTTPConnection('localhost', 8080)
    mac = ''
    for i in range(0, 32):
        char = None
        maxTime = 0
        for a in alphabet:
            current = mac + a
            get = generate_url(filename, current)
            elapsed = 0
            for j in range(0, 70):
                h1.request('GET', get)
                t = timer()
                h1.getresponse()
                elapsed += timer() - t
            if maxTime < elapsed:
                maxTime = elapsed
                char = a
#            print(elapsed)
        mac += char
        print(mac)
    get = generate_url(filename, mac)
    print(mac)
    h1.request('GET', get)
    r = h1.getresponse()
    if r.code != 200:
        print('error')
    else:
        print('success')


if __name__ == '__main__':
    run('nodarius')
