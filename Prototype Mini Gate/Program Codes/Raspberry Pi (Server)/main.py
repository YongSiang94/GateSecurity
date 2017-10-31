import Stepper
import SocketServer
import encrypt

# Stepper.open() to spin in anti-clockwise
# Stepper.close() to spin in clockwise

while True:
    connection = SocketServer.setupConnection()
    SocketServer.receiveIV(connection)
    data = SocketServer.dataTransfer(connection)
    data = encrypt.decrypt(data)
    if (data == 'open'):
	print('Opening')
	Stepper.open()
    elif (data == 'close'):
	print('Closing')
	Stepper.close()
