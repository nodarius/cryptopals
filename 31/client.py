#!/usr/bin/python3

import http.client

def run():
    h1 = http.client.HTTPConnection('localhost', 8080)
    h1.request('GET', '/?file=nodarius&mac=nodariusmac')
    
    r = h1.getresponse()
    print(r.code)
    pass

if __name__ == '__main__':
    run()
