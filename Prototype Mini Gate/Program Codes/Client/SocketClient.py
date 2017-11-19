import socket
import sys
import string
import encrypt
import time

socketPort = 17177
socketIP = '192.168.86.192'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((socketIP, socketPort))

def connectionToPi():
    global sock

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((socketIP, socketPort))

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

def reestablishAndSend():
    global message    
    
    encrypt.generateIV()
    message = encrypt.iv
    time.sleep(0.5)
    sock.sendall(message)
    sendCommand()

while True:
    reestablishAndSend()
    time.sleep(5)
    connectionToPi()
