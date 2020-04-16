import os
import sys
import logging
import time
import threading
import traceback

import soco
import RPi.GPIO as GPIO

import settings
from rotary.rotary_thread import RotaryThread
#from httpd.server import Server


logger = logging.getLogger('piradio')

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

WAIT_SEC = 0.8

stop_lock = threading.Lock()
play_lock = threading.Lock()


sonos_device = soco.discovery.any_soco()


######################################################################
# Callbacks
######################################################################


def sonos_previous():
    sonos_device.previous()
    pos = sonos_device.get_current_track_info()['playlist_position']
    logger.info("[ PREVIOUS ] %d" % pos)


def sonos_next():
    sonos_device.next()
    pos = sonos_device.get_current_track_info()['playlist_position']
    logger.info("[ NEXT ] %d" % pos)


def sonos_stop(ev=None):
    if stop_lock.acquire(False):
        logger.info("[ STOP ]")
        sonos_device.stop()
        time.sleep(WAIT_SEC)
        stop_lock.release()


def sonos_voldown():
    sonos_device.volume -= 4
    logger.info("[ VOLUME Down ] %d" % sonos_device.volume)


def sonos_volup():
    sonos_device.volume += 4
    logger.info("[ VOLUME UP ] %d" % sonos_device.volume)


def sonos_play(ev=None):
    if play_lock.acquire(False):
        # play_state can be 'PLAYING', 'PAUSED_PLAYBACK', or 'STOPPED'
        play_state = sonos_device.get_current_transport_info()['current_transport_state']
        if play_state == 'PLAYING':
            logger.info("[ PAUSE ]")
            sonos_device.pause()
            time.sleep(WAIT_SEC)
        else:
            logger.info("[ PLAY ]")
            sonos_device.play()
            time.sleep(WAIT_SEC5)
        play_lock.release()


def get_fav_uri():
    # Grab the URI that is at the top of our favorites list
    uri = None
    favs = sonos_device.get_sonos_favorites()
    if 'favorites' in favs and len(favs) > 0:
        uri = favs['favorites'][0]['uri']
    return uri


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
                rotary1_thread.setLeftCallback(sonos_voldown)
                rotary1_thread.setRightCallback(sonos_volup)
                rotary1_thread.setPushCallback(sonos_stop)
                rotary1_thread.start()

            if not rotary2_thread or not rotary2_thread.is_alive():
                logger.info("Starting rotary2 thread")
                rotary2_thread = RotaryThread("Rotary2", settings.ROTARY2_APin, settings.ROTARY2_BPin, settings.ROTARY2_SPin, logger)
                rotary2_thread.setLeftCallback(sonos_previous)
                rotary2_thread.setRightCallback(sonos_next)
                rotary2_thread.setPushCallback(sonos_play)
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
