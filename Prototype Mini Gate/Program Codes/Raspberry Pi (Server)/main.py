import Stepper
import SocketServer
import encrypt

# Stepper.open() to spin in anti-clockwise
# Stepper.close() to spin in clockwise

encrypted = ''

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
	print('Data received is: ' + encrypted)
	print('Opening')
	Stepper.open()
    elif (data == 'close'):
	print('Data received is: ' + encrypted)
	print('Closing')
	Stepper.close()
    elif (data == 'exit'):
	print('Client exited, re-establishing connection')
	establishConnection()
    else:
	print("Invalid command")
