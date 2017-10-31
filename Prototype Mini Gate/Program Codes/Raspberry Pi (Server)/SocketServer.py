import socket
from Crypto import Random
import encrypt

host = ''
port = 5680

def setupServer():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created")

    try:
	   s.bind((host, port))
    except socket.error as msg:
	   print(msg)
  
    print("Socket bind complete")
    return s

def setupConnection():
    s.listen(1) # listen only to one host
    conn, address = s.accept()
    print("Connected to: " + address[0] + ":" + str(address[1]))
    return conn

def dataTransfer(connection):
    data = connection.recv(1024)
    #data = data.decode('UTF-8', 'strict')
    print(data)
    return data
    connection.close()

def receiveIV(connection):
    iv = connection.recv(2048)
    print("Received: " + iv)
    encrypt.iv = iv

s = setupServer()
