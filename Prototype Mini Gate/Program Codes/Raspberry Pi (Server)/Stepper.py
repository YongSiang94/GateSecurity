import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
    
# Corresponding to INT1, INT2, INT3, and INT4
RPiPins = [7, 11, 13, 15]

# Set up pins
def setPins():
    for pin in RPiPins:
    	GPIO.setup(pin, GPIO.OUT)
    	GPIO.output(pin, False)

indexOfStepSequence = 0

# Default speed: 0.001 (Max speed)
speedOfRevolution = 0.001

# Default revolution count: 1
numOfRevolution = 4096


stepSequence = [[1, 0, 0, 0],
                [1, 1, 0, 0],
                [0, 1, 0, 0],
                [0, 1, 1, 0],
                [0, 0, 1, 0],
                [0, 0, 1, 1],
                [0, 0, 0, 1],
                [1, 0, 0, 1]]
   
def transverseSequence():
    for pin in range(0,4):
        patternPin = RPiPins[pin]
    	if (stepSequence[indexOfStepSequence][pin] == 1):
            GPIO.output(patternPin, True)
	else:
  	    GPIO.output(patternPin, False)

def open():
    global indexOfStepSequence
    global speedOfRevolution
    global numOfRevolution

    GPIO.setmode(GPIO.BOARD)
    setPins()
    try:
    	for x in range(0, numOfRevolution):
            transverseSequence()
	
            # Anti-clockwise motion to open
            indexOfStepSequence -= 1
	
            if (indexOfStepSequence < 0):
                indexOfStepSequence = 7

            time.sleep(speedOfRevolution)
    finally:
	GPIO.cleanup();    

def close():
    global indexOfStepSequence
    global speedOfRevolution
    global numOfRevolution
   
    GPIO.setmode(GPIO.BOARD)
    setPins()
    try:
    	for x in range(0, numOfRevolution):
    	    transverseSequence()
        
            # Clockwise motion to close
            indexOfStepSequence += 1
	
            if (indexOfStepSequence > 7):
            	indexOfStepSequence = 0

            time.sleep(speedOfRevolution)
    finally:
	GPIO.cleanup()
