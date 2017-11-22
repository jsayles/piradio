import os
import sys
import logging
import time
import traceback
import RPi.GPIO as GPIO

import mpd
from PIL import Image
from PIL import ImageDraw
from Adafruit_LED_Backpack import BicolorMatrix8x8

import settings
from rotary.rotary_thread import RotaryThread
#from httpd.server import Server


logger = logging.getLogger('piradio')

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# display = BicolorMatrix8x8.BicolorMatrix8x8()
# display.begin()


######################################################################
# Display Functions
######################################################################


def fill_display(r, g):
    display.clear()
    image = Image.new('RGB', (8, 8))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 7, 7), fill=(r, g, 0))
    display.set_image(image)
    display.write_display()


def drawPixel(x, y, c):
    display.clear()
    display.set_pixel(x, y, c)
    display.write_display()


def splash():
    fill_display(255, 0)
    time.sleep(1)
    fill_display(0, 255)
    time.sleep(1)
    fill_display(255, 255)
    time.sleep(1)
    display.clear()
    display.write_display()


######################################################################
# MPD Functions
######################################################################


def getMPDClient():
    client = mpd.MPDClient(use_unicode=True)
    client.connect("localhost", 6600)
    return client


######################################################################
# Callbacks
######################################################################


def rotary1_left():
    logger.debug("rotary1_left")
    client = getMPDClient()
    client.previous()
    client.close()


def rotary1_right():
    logger.debug("rotary1_right")
    client = getMPDClient()
    client.next()
    client.close()


def rotary1_push(ev=None):
    logger.debug("rotary1_push")
    client = getMPDClient()
    client.pause()
    client.close()
    time.sleep(.5)


def rotary2_left():
    logger.debug("rotary2_left")
    client = getMPDClient()
    status = client.status()
    volume = int(status['volume'])
    client.setvol(volume - 1)
    client.close()


def rotary2_right():
    logger.debug("rotary2_right")
    client = getMPDClient()
    status = client.status()
    volume = int(status['volume'])
    client.setvol(volume + 1)
    client.close()


def rotary2_push(ev=None):
    logger.debug("rotary2_push")
    client = getMPDClient()
    client.pause()
    client.close()
    time.sleep(.5)


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

    # Splash the display
    # splash()

    rotary1_thread = None
    rotary2_thread = None
    # server = None

    loops = 0
    try:
        while True:
            loops = loops + 1
            logger.debug("Main Loop " + str(loops))

            # Make sure our rotary threads are alive and happy
            if not rotary1_thread or not rotary1_thread.is_alive():
                logger.info("Starting rotary1 thread")
                rotary1_thread = RotaryThread("Rotary1", settings.ROTARY1_APin, settings.ROTARY1_BPin, settings.ROTARY1_SPin, logger)
                rotary1_thread.setLeftCallback(rotary1_left)
                rotary1_thread.setRightCallback(rotary1_right)
                rotary1_thread.setPushCallback(rotary1_push)
                rotary1_thread.start()

            if not rotary2_thread or not rotary2_thread.is_alive():
                logger.info("Starting rotary2 thread")
                rotary2_thread = RotaryThread("Rotary2", settings.ROTARY2_APin, settings.ROTARY2_BPin, settings.ROTARY2_SPin, logger)
                rotary2_thread.setLeftCallback(rotary2_left)
                rotary2_thread.setRightCallback(rotary2_right)
                rotary2_thread.setPushCallback(rotary2_push)
                rotary2_thread.start()

            # if settings.HTTP_SERVER:
            #     if not server or not server.is_alive():
            #         logger.info("Starting HTTP server")
            #         server = Server(queue, logger)
            #         server.setDaemon(True)
            #         server.start()

            time.sleep(15)
    except KeyboardInterrupt:
        logger.info("Keyboard Interuption!")
    except Exception as e:
        logger.exception(e)
    finally:
        logger.debug("Shutting Down...")
        if rotary1_thread:
            rotary1_thread.stop()
            rotary1_thread.join()
        if rotary2_thread:
            rotary2_thread.stop()
            rotary2_thread.join()

    # Release GPIO
    GPIO.cleanup()


if __name__ == '__main__':
    main()
