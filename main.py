#!/usr/bin/python

try:
    import RPi.GPIO as GPIO
    PI = True
except ImportError:
    PI = False

import os
import sys
import logging
import time
import traceback

import settings
from rotary.rotary_thread import RotaryThread
#from httpd.server import Server

logger = logging.getLogger('piradio')

######################################################################
# Callbacks
######################################################################

def rotary1_left():
    logger.debug("rotary1_left")

def rotary1_right():
    logger.debug("rotary1_right")

def rotary1_push():
    logger.debug("rotary1_push")

def rotary2_left():
    logger.debug("rotary2_left")

def rotary2_right():
    logger.debug("rotary2_right")

def rotary2_push():
    logger.debug("rotary2_push")

######################################################################
# Main Loop
######################################################################

def main():
    # Setup Logging
    hdlr = logging.FileHandler(settings.LOG)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    hdlr = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    if settings.DEBUG:
        logger.setLevel(logging.DEBUG)
        logger.info("DEBUG level logging")
    else:
        logger.setLevel(logging.INFO)
        logger.info("INFO level logging")
        logger.info("Starting up...")

    if PI:
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        # Rotary Encoder 1
        GPIO.setup(settings.ROTARY1_APin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(settings.ROTARY1_BPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(settings.ROTARY1_SPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        # Rotary Encoder 2
        GPIO.setup(settings.ROTARY2_APin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(settings.ROTARY2_BPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(settings.ROTARY2_SPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        rotary1_thread = None
        rotary2_thread = None
        # server = None

        loops = 0
        while True:
            try:
                loops = loops + 1
                logger.debug("Main Loop " + str(loops))

                # Make sure our rotary threads are alive and happy
                if not rotary1_thread or not rotary1_thread.is_alive():
                    logger.info("Starting rotary1 thread")
                    rotary1_thread = RotaryThread(settings.ROTARY1_APin, settings.ROTARY1_BPin, settings.ROTARY1_SPin)
                    rotary1_thread.setLeftCallback(rotary1_left)
                    rotary1_thread.setRightCallback(rotary1_right)
                    rotary1_thread.setPushCallback(rotary1_push)
                    rotary1_thread.setDaemon(True)
                    rotary1_thread.start()

                    # if settings.HTTP_SERVER:
                    #     if not server or not server.is_alive():
                    #         logger.info("Starting HTTP server")
                    #         server = Server(queue, logger)
                    #         server.setDaemon(True)
                    #         server.start()

                    time.sleep(15)

                    logger.warn("Exiting main thread")
            finally:
                # Release resource
                GPIO.cleanup()

if __name__ == '__main__':
    main()
