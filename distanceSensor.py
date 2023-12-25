#Libraries
import RPi.GPIO as GPIO
import time
 
# Sensors pins setting
# ===== distance sensor pin setting ==================
distSensorTrigPin = 16
distSensorEchoPin = 18
# distance sensor connect the grn pin to GROUND (for example: pin 6)
# distance sensor connect the VCC pin to 5v pin#2
 
 
def cleanBoard():
    print("Cleaning up!")
    # Release resources - clean up the board setting
    GPIO.cleanup()
 
 
def setup():
    # Disable warnings (optional)
    GPIO.setwarnings(False)
    # set the GPIO to the BOARD mode
    GPIO.setmode(GPIO.BOARD)
    # Sensors Setting
    # ===== distance sensor pin setting ==================
    GPIO.setup(distSensorTrigPin, GPIO.OUT)
    GPIO.setup(distSensorEchoPin, GPIO.IN)
 
 
 
def distance(measure='cm'):
    try:
        GPIO.output(distSensorTrigPin, False)
        print("please wait a few seconds for the distance sensor to settle.")
        time.sleep(1)
        GPIO.output(distSensorTrigPin, True)
        time.sleep(0.00001)
 
        GPIO.output(distSensorTrigPin, False)
        #this is a loop that allows us to record the last timestamp before the signal reaches the receiver.
        while GPIO.input(distSensorEchoPin) == 0:
            noSignal = time.time()
 
        #here we register the last timestamp at which the receiver detects the signal. Namely,
        # the receiver will start receiving a direct signal until the reflected signal is finally received.
        while GPIO.input(distSensorEchoPin) == 1:
            signal = time.time()
 
        #we calculate the time difference between both timestamps
        timeLapse = signal - noSignal
 
        if measure == 'cm':
            distance = timeLapse / 0.000058
        elif measure == 'in':
            distance = timeLapse / 0.000148
        else:
            print('improper choice of measurement: in or cm')
            distance = None
        return round(distance)
    except:
        distance = -1
        return distance
 
 
 
# main part
if __name__ == "__main__":
    setup()
    try:
        while True:
            print(str(distance('cm'))+ ' cm')
    except KeyboardInterrupt:  # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program
        cleanBoard() 
