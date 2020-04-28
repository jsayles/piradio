import os
import time
import threading

# If this is run not on the pi it will fail
try:
    import RPi.GPIO as GPIO
except:
    pass


class RotaryThread(threading.Thread):

    def __init__(self, name, aPin, bPin, sPin, logger=None):
        threading.Thread.__init__(self)
        self.deamon = True
        self.name = name
        self.logger = logger
        self.run_flag = True
        self.aPin = aPin
        self.bPin = bPin
        self.sPin = sPin
        self.leftCallback = None
        self.rightCallback = None
        self.pushCallback = None
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.aPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.bPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.sPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def setPushCallback(self, callback):
        self.pushCallback = callback
        GPIO.add_event_detect(self.sPin, GPIO.FALLING, callback=callback)

    def setLeftCallback(self, callback):
        self.leftCallback = callback

    def setRightCallback(self, callback):
        self.rightCallback = callback

    def stop(self):
        self.run_flag = False

    def run(self):
        if logger:
            self.logger.debug("%s: Starting thread loop" % self.name)
        last_b = 0
        current_b = 0
        check_values = False

        try:
            while self.run_flag:
                last_b = GPIO.input(self.bPin)
                while(not GPIO.input(self.aPin)):
                    current_b = GPIO.input(self.bPin)
                    check_values = True
                if check_values:
                    check_values = False
                    if (last_b == 0) and (current_b == 1):
                        self.leftCallback()
                    if (last_b == 1) and (current_b == 0):
                        self.rightCallback()
        except Exception as e:
            if logger:
                self.logger.error(e)
            self.stop()

        if logger:
            self.logger.info("%s: Exiting" % self.name)
        GPIO.cleanup()
