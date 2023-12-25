#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  ergonomic_pro.py
#  

#imported libraries
import RPi.GPIO as GPIO
import time

#set up pins

#==========LED pin=========
redLedPin = 12 #longer leg
#groundpin = 6 smaller leg

#==========5V Buzzer=======
buzzerPin = 22
#groundpin = 14

#======Distance Sensor=====
distSensorTrigPin = 16
distSensorEchoPin = 18
#VCCpin= 2 (power)
#groundpin = 20

#=======Tilt Sensor========
leftTiltPin = 29
rightTiltPin =  31
#groundpin = 9
#VCCpin = 4 (power)


def setup():
    # Disable warnings (optional)
    GPIO.setwarnings(False)
    # set the GPIO to the BOARD mode
    GPIO.setmode(GPIO.BOARD)
    # ===== LED sensor pin setting ==================
    GPIO.setup(redLedPin, GPIO.OUT)
    # ===== buzzer pin setting ==================
    GPIO.setup(buzzerPin, GPIO.OUT)
    # ===== distance sensor pin setting ==================
    GPIO.setup(distSensorTrigPin, GPIO.OUT)
    GPIO.setup(distSensorEchoPin, GPIO.IN)
    # ====== tilt sensor ==================
    GPIO.setup(leftTiltPin, GPIO.IN)
    GPIO.setup(rightTiltPin, GPIO.IN)
    # Bottom pin mode is input, and pull up to high level (3.3 v)
    GPIO.setup(leftTiltPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(rightTiltPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(leftTiltPin, GPIO.FALLING, callback=checkLeftTilt, bouncetime=200)
    GPIO.add_event_detect(rightTiltPin, GPIO.FALLING, callback=checkRightTilt, bouncetime=200)

def cleanBoard():
    print("Cleaning up!")
    # Release resources - clean up the board setting
    GPIO.cleanup()


def checkLeftTilt(null):
    print('Tilted on one side')
    alertOn()
    print("Fix the position\n")
    time.sleep(1)
    clearAlert()
    '''
    if (GPIO.input(leftTiltPin)):
        return True
    else:
        return False
    '''

def checkRightTilt(null):
    print('Tilted on other side')
    alertOn()
    print("Fix the position\n")
    time.sleep(1)
    clearAlert()

    '''
    if (GPIO.input(rightTiltPin)):
        return True
    else:
        return False
    '''
    
def LEDOn():
    #turning the light on
    GPIO.output(redLedPin, GPIO.HIGH)

def LEDOff():
    #turning the light off
    GPIO.output(redLedPin, GPIO.LOW)
    
def BeepOn():
    GPIO.output(buzzerPin, GPIO.HIGH)
    
def BeepOff():
    GPIO.output(buzzerPin, GPIO.LOW)


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
    
    
def getUserArmLength():
    userArmLength = 0
    
    while True:
        try:
            userArmLength = int(input("Input the user's arm distance in cm: "))
        except ValueError:
            print("\nYou're inputted value is not an integer. Please try again")
            continue
        if userArmLength in range(20,120):
            return userArmLength
            break
        else:
            print("\nYour inputted value is not in the correct range. Please try again.")

def alertOn():
    LEDOn()
    BeepOn()
    time.sleep(0.5)
    BeepOff()

def clearAlert():
    BeepOff()
    LEDOff()
    
def TestLED():
	for p in range(1,6):
		print("Red")
		LEDOn()
		time.sleep(0.5) #delay by 5 seconds
		LEDOff()
		time.sleep(0.5) #delay by 5 seconds

def TestBuzzer():
    for i in range (1, 6):
        print("Beepo")
        BeepOn()
        time.sleep(0.5)  #delay in 5 sec
        print("No Beepo")
        BeepOff()
        time.sleep(0.5)

def RelaxTime(pauseTimeSec):
    startTime = time.time()
    print('Sensors are relaxing for {} for seconds'.format(pauseTimeSec))
    time.sleep(pauseTimeSec - ( ( time.time() - startTime) % pauseTimeSec ))
    print('Cheking positions....\n')


def TiltTest():
    ArmLength = getUserArmLength()
    print("\nThe user should approximateley " + str(ArmLength) + " cm away from the monitor.")
    
    try:
        while True:
            print("while loop\n")

            '''
            if checkLeftTilt():
                print("Left tilted\n")
                alertOn()
                print("Fix the position\n")
                time.sleep(1)
                clearAlert()
            elif checkRightTilt():    
                print("Right tilted\n")
                alertOn()
                print("Fix the position\n")
                time.sleep(1)
                clearAlert()
            '''
            RealDistance = distance('cm')
            print( str(RealDistance) + ' cm')
            if RealDistance not in range((ArmLength - 3),(ArmLength + 3)):
                alertOn()
                print("Fix the position\n")
                time.sleep(1)
                clearAlert()
            else:
                print("Horizontal and a safe distance away from the screen \n")
                clearAlert()
                RelaxTime(10.0)
             
    except KeyboardInterrupt:  # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program
        clearAlert()


if __name__ == '__main__':
    setup()
    #TestLED()
    #TestBuzzer()
    TiltTest()
    cleanBoard()



    
