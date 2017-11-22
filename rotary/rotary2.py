#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

RoAPin = 27
RoBPin = 22
RoSPin = 25

globalCounter = 0

flag = 0
Last_RoB_Status = 0
Current_RoB_Status = 0


def setCounter(diff):
        global globalCounter
	sleep_ms = 0.1
        if diff == 0:
                globalCounter = 0
		sleep_ms = 1
        else:
                globalCounter = globalCounter + diff
        print 'globalCounter = %d' % globalCounter
        time.sleep(sleep_ms)


# Callback for clear button
def clear_callback(ev=None):
        setCounter(0)


def setup():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(RoAPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(RoBPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(RoSPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.add_event_detect(RoSPin, GPIO.FALLING, callback=clear_callback)


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
			setCounter(1)
			#globalCounter = globalCounter + 1
			#print 'globalCounter = %d' % globalCounter
		if (Last_RoB_Status == 1) and (Current_RoB_Status == 0):
			setCounter(-1)
			#globalCounter = globalCounter - 1
			#print 'globalCounter = %d' % globalCounter


def loop():
	while True:
		rotaryDeal()


def destroy():
	GPIO.cleanup()             # Release resource


if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()
