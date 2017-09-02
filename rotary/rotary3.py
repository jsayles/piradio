#!/usr/bin/env python
import RPi.GPIO as GPIO
import time


RoAPin =  4    # pin11
RoBPin = 17    # pin12
RoSPin = 18    # pin13

globalCounter = 0


def setCounter(diff):
	global globalCounter
	if diff == 0:
        	globalCounter = 0
	else:
		globalCounter = globalCounter + diff
	#print 'globalCounter = %d' % globalCounter
	time.sleep(1)


def clear(ev=None):
	setCounter(0)


def markTurnLeft():
	setCounter(1)


def markTurnRight():
	setCounter(-1)


def markA(ev=None):
	a = GPIO.input(RoAPin)
	b = GPIO.input(RoBPin)
	if a and not b:
		markTurnLeft()
	elif b and not a:
		markTurnRight()
	print("marcA(): a=%d, b=%d, c=%d" %(a,b,globalCounter))


def markB(ev=None):
	a = GPIO.input(RoAPin)
	b = GPIO.input(RoBPin)
	#print("marcB(): a=%d, b=%d" %(a,b))
	if b and not a:
		markTurnLeft()
	elif a and not b:
		markTurnRight()
	print("marcB(): a=%d, b=%d, c=%d" %(a,b,globalCounter))


def setup():
	GPIO.setmode(GPIO.BCM)

	GPIO.setup(RoAPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(RoAPin, GPIO.BOTH, callback=markA)

	GPIO.setup(RoBPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(RoBPin, GPIO.BOTH, callback=markB)

	GPIO.setup(RoSPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(RoSPin, GPIO.RISING, callback=clear)


def rotaryDeal():
	global flag
	global Last_RoB_Status
	global Current_RoB_Status
	global globalCounter
	Last_RoB_Status = GPIO.input(RoBPin)
	while(not GPIO.input(RoAPin)):
		Current_RoB_Status = GPIO.input(RoBPin)
		flag = 1
	if flag == 1:
		flag = 0
		if (Last_RoB_Status == 0) and (Current_RoB_Status == 1):
			globalCounter = globalCounter + 1
			print 'globalCounter = %d' % globalCounter
		if (Last_RoB_Status == 1) and (Current_RoB_Status == 0):
			globalCounter = globalCounter - 1
			print 'globalCounter = %d' % globalCounter


def loop():
	global globalCounter
	while True:
		#rotaryDeal()
		time.sleep(0.01)

def destroy():
	GPIO.cleanup()             # Release resource


if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()
