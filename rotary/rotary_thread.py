import RPi.GPIO as GPIO
import threading
import time
import os


GPIO.setmode(GPIO.BCM)

class RotaryThread(threading.Thread):

    def __init__(self, aPin, bPin, sPin):
        threading.Thread.__init__(self)
        self.deamon = True

        self._globalCounter = 0
        self._flag = 0
        self._last_b = 0
        self._current_b = 0

        self.aPin = aPin
        self.bPin = bPin
        self.sPin = sPin

        self.leftCallback = None
        self.rightCallback = None
        self.pushCallback = None

    def setPushCallback(self, callback):
        self.pushCallback = callback
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.sPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.sPin, GPIO.FALLING, callback=callback)

    def setLeftCallback(self, callback):
        self.leftCallback = callback

    def setRightCallback(self, callback):
        self.rightCallback = callback

    def run(self):
        while True:
            try:
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(self.aPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                GPIO.setup(self.bPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                self._last_b = GPIO.input(self.bPin)
                while(not GPIO.input(self.aPin)):
                    self._current_b = GPIO.input(self.bPin)
                    self._flag = 1
                if self._flag == 1:
                    self._flag = 0
                    if (self._last_b == 0) and (self._current_b == 1):
                        self.leftCallback()
                    if (self._last_b == 1) and (self._current_b == 0):
                        self.rightCallback()
            finally:
                # Release resource
                try:
                    GPIO.cleanup()
                except Exception:
                    pass
                return
