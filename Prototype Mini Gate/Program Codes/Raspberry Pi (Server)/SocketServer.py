import socket
from Crypto import Random
import encrypt
import time

host = '192.168.86.192'
port = 17177

ivList = ['head']

def setupServer():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #print("Socket created")

    try:
	   s.bind((host, port))
    except socket.error as msg:
	   print(msg)
  
    #print("Socket bind complete")
    return s

def setupConnection():
    s.listen(1) # listen only to one host
    conn, address = s.accept()
    print("Connected to: " + address[0] + ":" + str(address[1]))
    return conn

def dataTransfer(connection):
    data = connection.recv(1024)
    return data

def receiveIV(connection):
    global ivList

    iv = connection.recv(2048)
    lenOfIdenticialIV = len(filter(lambda x: iv in x, ivList))
    if (lenOfIdenticialIV > 1):
	connection.close()
    else:
	ivList.append(iv)
	print("Current ivList contains: ")
    	print ivList
   	print("Received IV: " + iv)
    	encrypt.iv = iv

s = setupServer()
