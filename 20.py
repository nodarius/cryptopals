#!/usr/bin/python3

from Crypto.Cipher import AES
import string 
import base64
import struct
import random

def encrypt_ecb(key, string):
    return AES.new(key, AES.MODE_ECB, 'ignore').encrypt(string)

def decrypt_ecb(key, string):
    return AES.new(key, AES.MODE_ECB, 'ignore').decrypt(string)

def xor_encrypt(str, key):
    full_key = b''
    while(len(full_key) < len(str)):
        full_key += key
    l = [chr(a ^ b) for a, b in zip(str, full_key)]
    return ''.join(l).encode('latin')


def bits(i):
    return struct.pack('L', i)

def encrypt_ctr(key, text, nonce):
    nonce = bits(nonce)
    n = int(len(text) / 16) + 1
    encrypted = b''
    for i in range(0, n):
        block = nonce + bits(i)
        encrypted += encrypt_ecb(key, block)
    res = xor_encrypt(text, encrypted)
    return res

def decrypt_ctr(key, text, nonce):
    return encrypt_ctr(key, text, nonce)


def random_bytes(n):
    l = [chr(random.randint(0, 255)) for i in range(n)]
    l = ''.join(l)
    return l.encode('latin')


base64_list = [
    "SSdtIHJhdGVkICJSIi4uLnRoaXMgaXMgYSB3YXJuaW5nLCB5YSBiZXR0ZXIgdm9pZCAvIFBvZXRzIGFyZSBwYXJhbm9pZCwgREoncyBELXN0cm95ZWQ=",
    "Q3V6IEkgY2FtZSBiYWNrIHRvIGF0dGFjayBvdGhlcnMgaW4gc3BpdGUtIC8gU3RyaWtlIGxpa2UgbGlnaHRuaW4nLCBJdCdzIHF1aXRlIGZyaWdodGVuaW4nIQ==",
    "QnV0IGRvbid0IGJlIGFmcmFpZCBpbiB0aGUgZGFyaywgaW4gYSBwYXJrIC8gTm90IGEgc2NyZWFtIG9yIGEgY3J5LCBvciBhIGJhcmssIG1vcmUgbGlrZSBhIHNwYXJrOw==",
    "WWEgdHJlbWJsZSBsaWtlIGEgYWxjb2hvbGljLCBtdXNjbGVzIHRpZ2h0ZW4gdXAgLyBXaGF0J3MgdGhhdCwgbGlnaHRlbiB1cCEgWW91IHNlZSBhIHNpZ2h0IGJ1dA==",
    "U3VkZGVubHkgeW91IGZlZWwgbGlrZSB5b3VyIGluIGEgaG9ycm9yIGZsaWNrIC8gWW91IGdyYWIgeW91ciBoZWFydCB0aGVuIHdpc2ggZm9yIHRvbW9ycm93IHF1aWNrIQ==",
    "TXVzaWMncyB0aGUgY2x1ZSwgd2hlbiBJIGNvbWUgeW91ciB3YXJuZWQgLyBBcG9jYWx5cHNlIE5vdywgd2hlbiBJJ20gZG9uZSwgeWEgZ29uZSE=",
    "SGF2ZW4ndCB5b3UgZXZlciBoZWFyZCBvZiBhIE1DLW11cmRlcmVyPyAvIFRoaXMgaXMgdGhlIGRlYXRoIHBlbmFsdHksYW5kIEknbSBzZXJ2aW4nIGE=",
    "RGVhdGggd2lzaCwgc28gY29tZSBvbiwgc3RlcCB0byB0aGlzIC8gSHlzdGVyaWNhbCBpZGVhIGZvciBhIGx5cmljYWwgcHJvZmVzc2lvbmlzdCE=",
    "RnJpZGF5IHRoZSB0aGlydGVlbnRoLCB3YWxraW5nIGRvd24gRWxtIFN0cmVldCAvIFlvdSBjb21lIGluIG15IHJlYWxtIHlhIGdldCBiZWF0IQ==",
    "VGhpcyBpcyBvZmYgbGltaXRzLCBzbyB5b3VyIHZpc2lvbnMgYXJlIGJsdXJyeSAvIEFsbCB5YSBzZWUgaXMgdGhlIG1ldGVycyBhdCBhIHZvbHVtZQ==",
    "VGVycm9yIGluIHRoZSBzdHlsZXMsIG5ldmVyIGVycm9yLWZpbGVzIC8gSW5kZWVkIEknbSBrbm93bi15b3VyIGV4aWxlZCE=",
    "Rm9yIHRob3NlIHRoYXQgb3Bwb3NlIHRvIGJlIGxldmVsIG9yIG5leHQgdG8gdGhpcyAvIEkgYWluJ3QgYSBkZXZpbCBhbmQgdGhpcyBhaW4ndCB0aGUgRXhvcmNpc3Qh",
    "V29yc2UgdGhhbiBhIG5pZ2h0bWFyZSwgeW91IGRvbid0IGhhdmUgdG8gc2xlZXAgYSB3aW5rIC8gVGhlIHBhaW4ncyBhIG1pZ3JhaW5lIGV2ZXJ5IHRpbWUgeWEgdGhpbms=",
    "Rmxhc2hiYWNrcyBpbnRlcmZlcmUsIHlhIHN0YXJ0IHRvIGhlYXI6IC8gVGhlIFItQS1LLUktTSBpbiB5b3VyIGVhcjs=",
    "VGhlbiB0aGUgYmVhdCBpcyBoeXN0ZXJpY2FsIC8gVGhhdCBtYWtlcyBFcmljIGdvIGdldCBhIGF4IGFuZCBjaG9wcyB0aGUgd2Fjaw==",
    "U29vbiB0aGUgbHlyaWNhbCBmb3JtYXQgaXMgc3VwZXJpb3IgLyBGYWNlcyBvZiBkZWF0aCByZW1haW4=",
    "TUMncyBkZWNheWluZywgY3V6IHRoZXkgbmV2ZXIgc3RheWVkIC8gVGhlIHNjZW5lIG9mIGEgY3JpbWUgZXZlcnkgbmlnaHQgYXQgdGhlIHNob3c=",
    "VGhlIGZpZW5kIG9mIGEgcmh5bWUgb24gdGhlIG1pYyB0aGF0IHlvdSBrbm93IC8gSXQncyBvbmx5IG9uZSBjYXBhYmxlLCBicmVha3MtdGhlIHVuYnJlYWthYmxl",
    "TWVsb2RpZXMtdW5tYWthYmxlLCBwYXR0ZXJuLXVuZXNjYXBhYmxlIC8gQSBob3JuIGlmIHdhbnQgdGhlIHN0eWxlIEkgcG9zc2Vz",
    "SSBibGVzcyB0aGUgY2hpbGQsIHRoZSBlYXJ0aCwgdGhlIGdvZHMgYW5kIGJvbWIgdGhlIHJlc3QgLyBGb3IgdGhvc2UgdGhhdCBlbnZ5IGEgTUMgaXQgY2FuIGJl",
    "SGF6YXJkb3VzIHRvIHlvdXIgaGVhbHRoIHNvIGJlIGZyaWVuZGx5IC8gQSBtYXR0ZXIgb2YgbGlmZSBhbmQgZGVhdGgsIGp1c3QgbGlrZSBhIGV0Y2gtYS1za2V0Y2g=",
    "U2hha2UgJ3RpbGwgeW91ciBjbGVhciwgbWFrZSBpdCBkaXNhcHBlYXIsIG1ha2UgdGhlIG5leHQgLyBBZnRlciB0aGUgY2VyZW1vbnksIGxldCB0aGUgcmh5bWUgcmVzdCBpbiBwZWFjZQ==",
    "SWYgbm90LCBteSBzb3VsJ2xsIHJlbGVhc2UhIC8gVGhlIHNjZW5lIGlzIHJlY3JlYXRlZCwgcmVpbmNhcm5hdGVkLCB1cGRhdGVkLCBJJ20gZ2xhZCB5b3UgbWFkZSBpdA==",
    "Q3V6IHlvdXIgYWJvdXQgdG8gc2VlIGEgZGlzYXN0cm91cyBzaWdodCAvIEEgcGVyZm9ybWFuY2UgbmV2ZXIgYWdhaW4gcGVyZm9ybWVkIG9uIGEgbWljOg==",
    "THlyaWNzIG9mIGZ1cnkhIEEgZmVhcmlmaWVkIGZyZWVzdHlsZSEgLyBUaGUgIlIiIGlzIGluIHRoZSBob3VzZS10b28gbXVjaCB0ZW5zaW9uIQ==",
    "TWFrZSBzdXJlIHRoZSBzeXN0ZW0ncyBsb3VkIHdoZW4gSSBtZW50aW9uIC8gUGhyYXNlcyB0aGF0J3MgZmVhcnNvbWU=",
    "WW91IHdhbnQgdG8gaGVhciBzb21lIHNvdW5kcyB0aGF0IG5vdCBvbmx5IHBvdW5kcyBidXQgcGxlYXNlIHlvdXIgZWFyZHJ1bXM7IC8gSSBzaXQgYmFjayBhbmQgb2JzZXJ2ZSB0aGUgd2hvbGUgc2NlbmVyeQ==",
    "VGhlbiBub25jaGFsYW50bHkgdGVsbCB5b3Ugd2hhdCBpdCBtZWFuIHRvIG1lIC8gU3RyaWN0bHkgYnVzaW5lc3MgSSdtIHF1aWNrbHkgaW4gdGhpcyBtb29k",
    "QW5kIEkgZG9uJ3QgY2FyZSBpZiB0aGUgd2hvbGUgY3Jvd2QncyBhIHdpdG5lc3MhIC8gSSdtIGEgdGVhciB5b3UgYXBhcnQgYnV0IEknbSBhIHNwYXJlIHlvdSBhIGhlYXJ0",
    "UHJvZ3JhbSBpbnRvIHRoZSBzcGVlZCBvZiB0aGUgcmh5bWUsIHByZXBhcmUgdG8gc3RhcnQgLyBSaHl0aG0ncyBvdXQgb2YgdGhlIHJhZGl1cywgaW5zYW5lIGFzIHRoZSBjcmF6aWVzdA==",
    "TXVzaWNhbCBtYWRuZXNzIE1DIGV2ZXIgbWFkZSwgc2VlIGl0J3MgLyBOb3cgYW4gZW1lcmdlbmN5LCBvcGVuLWhlYXJ0IHN1cmdlcnk=",
    "T3BlbiB5b3VyIG1pbmQsIHlvdSB3aWxsIGZpbmQgZXZlcnkgd29yZCdsbCBiZSAvIEZ1cmllciB0aGFuIGV2ZXIsIEkgcmVtYWluIHRoZSBmdXJ0dXJl",
    "QmF0dGxlJ3MgdGVtcHRpbmcuLi53aGF0ZXZlciBzdWl0cyB5YSEgLyBGb3Igd29yZHMgdGhlIHNlbnRlbmNlLCB0aGVyZSdzIG5vIHJlc2VtYmxhbmNl",
    "WW91IHRoaW5rIHlvdSdyZSBydWZmZXIsIHRoZW4gc3VmZmVyIHRoZSBjb25zZXF1ZW5jZXMhIC8gSSdtIG5ldmVyIGR5aW5nLXRlcnJpZnlpbmcgcmVzdWx0cw==",
    "SSB3YWtlIHlhIHdpdGggaHVuZHJlZHMgb2YgdGhvdXNhbmRzIG9mIHZvbHRzIC8gTWljLXRvLW1vdXRoIHJlc3VzY2l0YXRpb24sIHJoeXRobSB3aXRoIHJhZGlhdGlvbg==",
    "Tm92b2NhaW4gZWFzZSB0aGUgcGFpbiBpdCBtaWdodCBzYXZlIGhpbSAvIElmIG5vdCwgRXJpYyBCLidzIHRoZSBqdWRnZSwgdGhlIGNyb3dkJ3MgdGhlIGp1cnk=",
    "WW8gUmFraW0sIHdoYXQncyB1cD8gLyBZbywgSSdtIGRvaW5nIHRoZSBrbm93bGVkZ2UsIEUuLCBtYW4gSSdtIHRyeWluZyB0byBnZXQgcGFpZCBpbiBmdWxs",
    "V2VsbCwgY2hlY2sgdGhpcyBvdXQsIHNpbmNlIE5vcmJ5IFdhbHRlcnMgaXMgb3VyIGFnZW5jeSwgcmlnaHQ/IC8gVHJ1ZQ==",
    "S2FyYSBMZXdpcyBpcyBvdXIgYWdlbnQsIHdvcmQgdXAgLyBaYWtpYSBhbmQgNHRoIGFuZCBCcm9hZHdheSBpcyBvdXIgcmVjb3JkIGNvbXBhbnksIGluZGVlZA==",
    "T2theSwgc28gd2hvIHdlIHJvbGxpbicgd2l0aCB0aGVuPyBXZSByb2xsaW4nIHdpdGggUnVzaCAvIE9mIFJ1c2h0b3duIE1hbmFnZW1lbnQ=",
    "Q2hlY2sgdGhpcyBvdXQsIHNpbmNlIHdlIHRhbGtpbmcgb3ZlciAvIFRoaXMgZGVmIGJlYXQgcmlnaHQgaGVyZSB0aGF0IEkgcHV0IHRvZ2V0aGVy",
    "SSB3YW5uYSBoZWFyIHNvbWUgb2YgdGhlbSBkZWYgcmh5bWVzLCB5b3Uga25vdyB3aGF0IEknbSBzYXlpbic/IC8gQW5kIHRvZ2V0aGVyLCB3ZSBjYW4gZ2V0IHBhaWQgaW4gZnVsbA==",
    "VGhpbmtpbicgb2YgYSBtYXN0ZXIgcGxhbiAvICdDdXogYWluJ3QgbnV0aGluJyBidXQgc3dlYXQgaW5zaWRlIG15IGhhbmQ=",
    "U28gSSBkaWcgaW50byBteSBwb2NrZXQsIGFsbCBteSBtb25leSBpcyBzcGVudCAvIFNvIEkgZGlnIGRlZXBlciBidXQgc3RpbGwgY29taW4nIHVwIHdpdGggbGludA==",
    "U28gSSBzdGFydCBteSBtaXNzaW9uLCBsZWF2ZSBteSByZXNpZGVuY2UgLyBUaGlua2luJyBob3cgY291bGQgSSBnZXQgc29tZSBkZWFkIHByZXNpZGVudHM=",
    "SSBuZWVkIG1vbmV5LCBJIHVzZWQgdG8gYmUgYSBzdGljay11cCBraWQgLyBTbyBJIHRoaW5rIG9mIGFsbCB0aGUgZGV2aW91cyB0aGluZ3MgSSBkaWQ=",
    "SSB1c2VkIHRvIHJvbGwgdXAsIHRoaXMgaXMgYSBob2xkIHVwLCBhaW4ndCBudXRoaW4nIGZ1bm55IC8gU3RvcCBzbWlsaW5nLCBiZSBzdGlsbCwgZG9uJ3QgbnV0aGluJyBtb3ZlIGJ1dCB0aGUgbW9uZXk=",
    "QnV0IG5vdyBJIGxlYXJuZWQgdG8gZWFybiAnY3V6IEknbSByaWdodGVvdXMgLyBJIGZlZWwgZ3JlYXQsIHNvIG1heWJlIEkgbWlnaHQganVzdA==",
    "U2VhcmNoIGZvciBhIG5pbmUgdG8gZml2ZSwgaWYgSSBzdHJpdmUgLyBUaGVuIG1heWJlIEknbGwgc3RheSBhbGl2ZQ==",
    "U28gSSB3YWxrIHVwIHRoZSBzdHJlZXQgd2hpc3RsaW4nIHRoaXMgLyBGZWVsaW4nIG91dCBvZiBwbGFjZSAnY3V6LCBtYW4sIGRvIEkgbWlzcw==",
    "QSBwZW4gYW5kIGEgcGFwZXIsIGEgc3RlcmVvLCBhIHRhcGUgb2YgLyBNZSBhbmQgRXJpYyBCLCBhbmQgYSBuaWNlIGJpZyBwbGF0ZSBvZg==",
    "RmlzaCwgd2hpY2ggaXMgbXkgZmF2b3JpdGUgZGlzaCAvIEJ1dCB3aXRob3V0IG5vIG1vbmV5IGl0J3Mgc3RpbGwgYSB3aXNo",
    "J0N1eiBJIGRvbid0IGxpa2UgdG8gZHJlYW0gYWJvdXQgZ2V0dGluJyBwYWlkIC8gU28gSSBkaWcgaW50byB0aGUgYm9va3Mgb2YgdGhlIHJoeW1lcyB0aGF0IEkgbWFkZQ==",
    "U28gbm93IHRvIHRlc3QgdG8gc2VlIGlmIEkgZ290IHB1bGwgLyBIaXQgdGhlIHN0dWRpbywgJ2N1eiBJJ20gcGFpZCBpbiBmdWxs",
    "UmFraW0sIGNoZWNrIHRoaXMgb3V0LCB5byAvIFlvdSBnbyB0byB5b3VyIGdpcmwgaG91c2UgYW5kIEknbGwgZ28gdG8gbWluZQ==",
    "J0NhdXNlIG15IGdpcmwgaXMgZGVmaW5pdGVseSBtYWQgLyAnQ2F1c2UgaXQgdG9vayB1cyB0b28gbG9uZyB0byBkbyB0aGlzIGFsYnVt",
    "WW8sIEkgaGVhciB3aGF0IHlvdSdyZSBzYXlpbmcgLyBTbyBsZXQncyBqdXN0IHB1bXAgdGhlIG11c2ljIHVw",
    "QW5kIGNvdW50IG91ciBtb25leSAvIFlvLCB3ZWxsIGNoZWNrIHRoaXMgb3V0LCB5byBFbGk=",
    "VHVybiBkb3duIHRoZSBiYXNzIGRvd24gLyBBbmQgbGV0IHRoZSBiZWF0IGp1c3Qga2VlcCBvbiByb2NraW4n",
    "QW5kIHdlIG91dHRhIGhlcmUgLyBZbywgd2hhdCBoYXBwZW5lZCB0byBwZWFjZT8gLyBQZWFjZQ=="]


def find_smallest_size(lst):
    return len(min(lst, key=len))

def truncate_items(lst, size):
    size = find_smallest_size(lst)
    res = []
    for item in lst:
        res.append(item[:size])
    return res


def encrypt_with_fixed_nonce(base64lst, nonce, key):
    res = []
    for b64 in base64lst:
        plain = base64.b64decode(b64)
        enc = encrypt_ctr(key, plain, nonce)
        res.append(enc)
    return res


def letter_frequency(string, letter):
    res = string.decode('latin').count(letter) / len(string)
    return res * 100

def evaluate_str_of_first_letters(str):
    result = 0

    for c in str:
        if chr(c) not in string.printable:
            result -= 1000 / len(str)

    result -= abs(7.5 - letter_frequency(str, 'A'))
    result -= abs(7.0 - letter_frequency(str, 'E'))
    result -= abs(5.1 - letter_frequency(str, 'O'))
    result -= abs(4.9 - letter_frequency(str, 'R'))
    result -= abs(4.6 - letter_frequency(str, 'I'))
    result -= abs(4.6 - letter_frequency(str, 'S'))
    result -= abs(4.5 - letter_frequency(str, 'N'))
    result -= abs(3.8 - letter_frequency(str, 'T'))
    result -= abs(3.7 - letter_frequency(str, 'L'))
    result -= abs(3.0 - letter_frequency(str, 'M'))
    result -= abs(2.7 - letter_frequency(str, 'D'))
    result -= abs(2.5 - letter_frequency(str, 'C'))
    result -= abs(2.4 - letter_frequency(str, 'P'))
    result -= abs(2.4 - letter_frequency(str, 'H'))
    result -= abs(2.2 - letter_frequency(str, 'B'))
    result -= abs(2.1 - letter_frequency(str, 'U'))
    result -= abs(1.9 - letter_frequency(str, 'K'))
    result -= abs(1.8 - letter_frequency(str, 'G'))
    result -= abs(1.5 - letter_frequency(str, 'Y'))
    result -= abs(1.2 - letter_frequency(str, 'F'))
    result -= abs(1.2 - letter_frequency(str, 'W'))
    result -= abs(0.8 - letter_frequency(str, 'J'))
    result -= abs(0.8 - letter_frequency(str, 'V'))
    result -= abs(0.6 - letter_frequency(str, 'Z'))
    result -= abs(0.5 - letter_frequency(str, 'X'))
    result -= abs(0.3 - letter_frequency(str, 'Q'))

    for i in range(0, 255):
        if i < ord('A') or i > ord('Z'):
            result - 10 * letter_frequency(str, chr(i))
    return result



def evaluate_str_of_not_first_letter(str):
    result = 0

    for c in str:
        if chr(c) not in string.printable:
            result -= 1000 / len(str)
                
    result -= abs(0 - letter_frequency(str, '0'))
    result -= abs(0 - letter_frequency(str, '1'))
    result -= abs(0 - letter_frequency(str, '2'))
    result -= abs(0 - letter_frequency(str, '3'))
    result -= abs(0 - letter_frequency(str, '3'))
    result -= abs(0 - letter_frequency(str, '4'))
    result -= abs(0 - letter_frequency(str, '5'))
    result -= abs(0 - letter_frequency(str, '6'))
    result -= abs(0 - letter_frequency(str, '7'))
    result -= abs(0 - letter_frequency(str, '8'))
    result -= abs(0 - letter_frequency(str, '9'))


    result -= abs(6.1 - letter_frequency(str, ' '))
    result -= abs(7.5 - letter_frequency(str, 'a'))
    result -= abs(7.0 - letter_frequency(str, 'e'))
    result -= abs(5.1 - letter_frequency(str, 'o'))
    result -= abs(4.9 - letter_frequency(str, 'r'))
    result -= abs(4.6 - letter_frequency(str, 'i'))
    result -= abs(4.6 - letter_frequency(str, 's'))
    result -= abs(4.5 - letter_frequency(str, 'n'))
    result -= abs(3.8 - letter_frequency(str, 't'))
    result -= abs(3.7 - letter_frequency(str, 'l'))
    result -= abs(3.0 - letter_frequency(str, 'm'))
    result -= abs(2.7 - letter_frequency(str, 'd'))
    result -= abs(2.5 - letter_frequency(str, 'c'))
    result -= abs(2.4 - letter_frequency(str, 'p'))
    result -= abs(2.4 - letter_frequency(str, 'h'))
    result -= abs(2.2 - letter_frequency(str, 'b'))
    result -= abs(2.1 - letter_frequency(str, 'u'))
    result -= abs(1.9 - letter_frequency(str, 'k'))
    result -= abs(1.8 - letter_frequency(str, 'g'))
    result -= abs(1.5 - letter_frequency(str, 'y'))
    result -= abs(1.2 - letter_frequency(str, 'f'))
    result -= abs(1.2 - letter_frequency(str, 'w'))
    result -= abs(0.8 - letter_frequency(str, 'j'))
    result -= abs(0.8 - letter_frequency(str, 'v'))
    result -= abs(0.6 - letter_frequency(str, 'z'))
    result -= abs(0.5 - letter_frequency(str, 'x'))
    result -= abs(0.3 - letter_frequency(str, 'q'))
    result -= abs(0.1 - letter_frequency(str, 'A'))
    result -= abs(0.1 - letter_frequency(str, 'S'))
    result -= abs(0.0 - letter_frequency(str, 'E'))
    result -= abs(0.0 - letter_frequency(str, 'R'))
    result -= abs(0.0 - letter_frequency(str, 'B'))
    result -= abs(0.0 - letter_frequency(str, 'T'))
    result -= abs(0.0 - letter_frequency(str, 'M'))
    result -= abs(0.0 - letter_frequency(str, 'L'))
    result -= abs(0.0 - letter_frequency(str, 'N'))
    result -= abs(0.0 - letter_frequency(str, 'P'))
    result -= abs(0.0 - letter_frequency(str, 'O'))
    result -= abs(0.0 - letter_frequency(str, 'I'))
    result -= abs(0.0 - letter_frequency(str, 'D'))
    result -= abs(0.0 - letter_frequency(str, 'C'))
    result -= abs(0.0 - letter_frequency(str, 'H'))
    result -= abs(0.0 - letter_frequency(str, 'G'))
    result -= abs(0.0 - letter_frequency(str, 'K'))
    result -= abs(0.0 - letter_frequency(str, 'F'))
    result -= abs(0.0 - letter_frequency(str, 'J'))
    result -= abs(0.0 - letter_frequency(str, 'U'))
    result -= abs(0.0 - letter_frequency(str, 'W'))
    result -= abs(0.0 - letter_frequency(str, 'Y'))
    result -= abs(0.0 - letter_frequency(str, 'V'))
    result -= abs(0.0 - letter_frequency(str, 'Z'))
    result -= abs(0.0 - letter_frequency(str, 'Q'))
    result -= abs(0.0 - letter_frequency(str, 'X'))

    result -= abs(0.0 - letter_frequency(str, '"'))
    result -= abs(0.0 - letter_frequency(str, ':'))
    result -= abs(0.0 - letter_frequency(str, '\\'))
    result -= abs(0.0 - letter_frequency(str, '&'))
    result -= abs(0.0 - letter_frequency(str, '='))
    result -= abs(0.0 - letter_frequency(str, '^'))
    result -= abs(0.0 - letter_frequency(str, ';'))
    result -= abs(0.0 - letter_frequency(str, '?'))
    result -= abs(0.0 - letter_frequency(str, '/'))
    result -= abs(0.0 - letter_frequency(str, '#'))
    result -= abs(0.0 - letter_frequency(str, '_'))
    result -= abs(0.0 - letter_frequency(str, '@'))
    result -= abs(0.0 - letter_frequency(str, '!'))
    result -= abs(0.0 - letter_frequency(str, '.'))
    result -= abs(0.0 - letter_frequency(str, '('))
    result -= abs(0.0 - letter_frequency(str, '-'))
    result -= abs(0.0 - letter_frequency(str, '+'))
    result -= abs(0.0 - letter_frequency(str, '\''))
    result -= abs(0.0 - letter_frequency(str, ')'))
    result -= abs(0.0 - letter_frequency(str, '$'))
    result -= abs(0.0 - letter_frequency(str, '*'))
    result -= abs(0.0 - letter_frequency(str, '%'))
    result -= abs(0.0 - letter_frequency(str, '{'))
    result -= abs(0.0 - letter_frequency(str, '}'))
    result -= abs(0.0 - letter_frequency(str, '`'))
    result -= abs(0.0 - letter_frequency(str, '~'))
    result -= abs(0.0 - letter_frequency(str, '|'))
    result -= abs(0.0 - letter_frequency(str, ','))
    result -= abs(0.0 - letter_frequency(str, '['))
    result -= abs(0.0 - letter_frequency(str, ']'))
    result -= abs(0.0 - letter_frequency(str, '<'))
    result -= abs(0.0 - letter_frequency(str, '>'))


    return result


def evaluate(str, is_first):
    if (len(str) == 0):
        return None
    if is_first:
        return evaluate_str_of_first_letters(str)
    else:
        return evaluate_str_of_not_first_letter(str)



def decode_single_byte_xor(encoded, is_first):
#    print(encoded)
    max_value = float("-inf")
    key_char = b''
    for i in range(0, 256):
        string = xor_encrypt(encoded, chr(i).encode('latin'))
        current_value = evaluate(string, is_first)
        if current_value > max_value:
            max_value = current_value
            key_char = chr(i).encode('latin')
    return key_char


def decode_repetead_key_xor(encoded, key_size):
    subs = list()
    for i in range(key_size):
        sub = b''
        for j in range(i, len(encoded), key_size):
            sub += chr(encoded[j]).encode('latin')
        subs.append(sub)

    key = b''
    is_first = True
    for sub in subs:
        key_char = decode_single_byte_xor(sub, is_first)
        is_first = False
        key += key_char
        print(".", end='', flush=True)
    print("")
    dec = xor_encrypt(encoded, key)
    print(dec)

    


def main():
    key = random_bytes(16)
    nonce = 0
    encs = encrypt_with_fixed_nonce(base64_list, nonce, key)
    key_size = find_smallest_size(encs)
    lst = truncate_items(encs, key_size)
    concatenated = b"".join(lst)
    decode_repetead_key_xor(concatenated, key_size)

main()
