import base64
import os
from Crypto.Cipher import AES
from Crypto import Random

key = '9369BE75CA85FA4CF63A9C581AD35646'
iv = ''

BS = 16

pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[:-ord(s[len(s)-1:])]

def encrypt(raw):
    raw = pad(raw)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(cipher.encrypt(raw))

def decrypt(encrypted):
    encrypted = base64.b64decode(encrypted)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(encrypted))

def generateIV():
    global BS
    global iv
    iv = Random.new().read(BS)
    print('IV generated for this session is ' + iv)
    return iv

#ciphertext = encrypt(user_input)
#plaintext = decrypt(ciphertext)

#print(ciphertext)
#print(plaintext)
