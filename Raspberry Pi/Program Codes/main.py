import Stepper
import SocketServer

# Stepper.open() to spin in anti-clockwise
# Stepper.close() to spin in clockwise

while True:
    connection = SocketServer.setupConnection()
    data = SocketServer.dataTransfer(connection)
    if (data == 'open'):
	print('Opening')
	Stepper.open()
    elif (data == 'close'):
	print('Closing')
	Stepper.close()
