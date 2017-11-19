import Stepper
import SocketServer
import encrypt
import time

# Stepper.open() to spin in anti-clockwise
# Stepper.close() to spin in clockwise

encrypted = ''
invalidAttempts = 0

connection = SocketServer.setupConnection()
SocketServer.receiveIV(connection)

def establishConnection():
    global connection
    connection = SocketServer.setupConnection()
    SocketServer.receiveIV(connection)

while True:
    encrypted = SocketServer.dataTransfer(connection)
    data = encrypt.decrypt(encrypted)
    if (data == 'open'):
	invalidAttempts = 0
    	print('Data received is: ' + encrypted)
    	print('Opening')
     	Stepper.open()
    	print("Establishing new socket!")
    	establishConnection()
    elif (data == 'close'):
    	invalidAttempts = 0
    	print('Data received is: ' + encrypted)
    	print('Closing')
    	Stepper.close()
    	print("Establishing new socket!")
    	establishConnection()
    elif (data == 'exit'):
    	invalidAttempts = 0
    	print('Client exited, re-establishing connection')
    	establishConnection()
    else:
	print("Invalid command received. Re-establishing connection")
	establishConnection()
