#!/usr/bin/python

try:
    import RPi.GPIO as GPIO
    PI = True
except ImportError:
    PI = False

import logging
import time
import os
from watcher import Watcher
from printer import Printer
from httpd.server import Server
from video import SLIDE
import sys
import traceback
import settings

def main():
    # Setup Logging
    logger = logging.getLogger('piradio')
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
        # Not interested
        GPIO.setwarnings(False)

        # Use BCM GPIO numbers
        GPIO.setmode(GPIO.BCM)

        # Setup the alert light
        if settings.LIGHT_PIN_1:
        GPIO.setup(settings.LIGHT_PIN_1, GPIO.OUT)
        GPIO.output(settings.LIGHT_PIN_1, GPIO.LOW)

        if settings.LIGHT_PIN_2:
        GPIO.setup(settings.LIGHT_PIN_2, GPIO.OUT)
        GPIO.output(settings.LIGHT_PIN_2, GPIO.LOW)


        # The queue is where messages go to be displayed
        queue = Queue.PriorityQueue()

        watcher = None
        printer = None
        server = None
        loops = 0
        while True:
        try:
        loops = loops + 1
        logger.debug("Main Loop " + str(loops))

        # Make sure our twitter thread is alive and happy
        if not watcher or not watcher.is_alive():
        logger.info("Starting watcher thread")
        watcher = Watcher(queue, logger)
        watcher.setDaemon(True)
        watcher.start()

        # Make sure our printing thread is alive and happy
        if not printer or not printer.is_alive():
        logger.info("Starting printer thread")
        printer = Printer(queue, logger, PI)
        printer.setDaemon(True)
        printer.start()

        if settings.HTTP_SERVER:
        if not server or not server.is_alive():
        logger.info("Starting HTTP server")
        server = Server(queue, logger)
        server.setDaemon(True)
        server.start()


        # Throw some info in the queue if it's getting low
        if queue.qsize() < 1:
        messages = open(settings.MSG_FILE, 'r')
        for msg in messages:
        queue.put((settings.PRIORITY_LOW, msg, "", False))
        messages.close()

        if settings.SLIDE_DIR:
        for filename in os.listdir(settings.SLIDE_DIR):
        queue.put((settings.PRIORITY_LOW, os.path.join(settings.SLIDE_DIR, filename), SLIDE, False))
        except Exception as e:
        logger.exception("Exception in main thread: " + str(e))

        time.sleep(15)

        logger.warn("Exiting main thread")


if __name__ == '__main__':
    main()
