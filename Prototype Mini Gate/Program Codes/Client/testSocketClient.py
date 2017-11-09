import socket
import sys
import string
import encrypt
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('192.168.86.184', 7777))

message = ''

def sendCommand():
    message2 = raw_input("Enter command: ")
    if (message2 == "exit"):
	sock.sendall(encrypt.encrypt(message2))
	sock.close()
	quit()
    print("Command received is: " + message2)
    encryptedMessage = encrypt.encrypt(message2)
    print("The encrypted version that will be sent is: " + encryptedMessage)
    sock.sendall(encryptedMessage)

message = encrypt.iv
time.sleep(0.5)
sock.sendall(message)
while True:
    sendCommand()
