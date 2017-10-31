import socket
import sys
import string
import encrypt

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('192.168.86.145', 5680))

message = ''

try:
    #message = raw_input("Enter command: ")
    #print(message)
    message = encrypt.iv
    #message = message.encode('UTF-8', 'strict')
    sock.sendall(message)

    message2 = raw_input("Enter command: ")
    print(message2)
    encrypted = encrypt.encrypt(message2)
    print("Encrypted: " + encrypted)
    sock.sendall(encrypted)
    print("Decrypted: " + encrypt.decrypt(encrypted))
finally:
    sock.close()
