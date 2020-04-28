import os
import sys
import logging
import time
import threading
import traceback

import soco

import settings
import sonos_utils
from rotary.rotary_thread import RotaryThread


logger = logging.getLogger('piradio')

thread_lock = threading.Lock()

sonos_device = sonos_utils.find_sonos()


######################################################################
# Rotary Knob Callbacks
######################################################################


def sonos_voldown():
    sonos_device.volume -= 4
    logger.info("[ VOLUME Down ] %d" % sonos_device.volume)


def sonos_volup():
    sonos_device.volume += 4
    logger.info("[ VOLUME UP ] %d" % sonos_device.volume)


def sonos_previous():
    sonos_device.previous()
    track = sonos_device.get_current_track_info()
    track_title = ""
    if track and 'title' in track:
        track_title = track['title']
    logger.info(f"[ PREVIOUS ] {track_title}" )


def sonos_next():
    sonos_device.next()
    track = sonos_device.get_current_track_info()
    track_title = ""
    if track and 'title' in track:
        track_title = track['title']
    logger.info(f"[ NEXT ] {track_title}" )


def sonos_stop(ev=None):
    if thread_lock.acquire(False):
        logger.info("[ STOP ]")
        sonos_device.stop()
        time.sleep(1)
        thread_lock.release()


def sonos_play(ev=None):
    if thread_lock.acquire(False):
        logger.info("[ PLAY ]")
        sonos_device.play()
        time.sleep(1)
        thread_lock.release()


def sonos_pause(ev=None):
    if thread_lock.acquire(False):
        logger.info("[ PAUSE ]")
        sonos_device.pause()
        time.sleep(1)
        thread_lock.release()


def sonos_play_pause(ev=None):
    if thread_lock.acquire(False):
        # play_state can be 'PLAYING', 'PAUSED_PLAYBACK', or 'STOPPED'
        play_state = sonos_device.get_current_transport_info()['current_transport_state']
        if play_state == 'PLAYING':
            logger.info("[ PAUSE ]")
            sonos_device.pause()
            time.sleep(0.8)
        else:
            logger.info("[ PLAY ]")
            sonos_device.play()
            time.sleep(0.8)
        thread_lock.release()


######################################################################
# Thread helper methods
######################################################################


def check_thread(thread, settings, logger):
    if not thread or not thread.is_alive():
        logger.info(f"Starting {settings.name} thread")
        thread = RotaryThread(name, settings['apin'], settings['bpin'], settings['spin'], logger=logger)
        thread.setLeftCallback(settings['left'])
        thread.setRightCallback(settings['right'])
        thread.setPushCallback(settings['push'])
        thread.start()
    return thread


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
    rotary1_settings = {
        'name': 'Rotary1',
        'apin': settings.ROTARY1_APin,
        'bpin': settings.ROTARY1_BPin,
        'spin': settings.ROTARY1_SPin,
        'left': sonos_voldown,
        'right': sonos_volup,
        'push': sonos_pause,
    }

    rotary2_thread = None
    rotary2_settings = {
        'name': 'Rotary2',
        'apin': settings.ROTARY2_APin,
        'bpin': settings.ROTARY2_BPin,
        'spin': settings.ROTARY2_SPin,
        'left': sonos_previous,
        'right': sonos_next,
        'push': sonos_stop,
    }

    rotary3_thread = None
    rotary3_settings = {
        'name': 'Rotary3',
        'apin': settings.ROTARY3_APin,
        'bpin': settings.ROTARY3_BPin,
        'spin': settings.ROTARY3_SPin,
        'left': sonos_previous,
        'right': sonos_next,
        'push': sonos_play,
    }

    loops = 0
    try:
        while True:
            loops = loops + 1
            logger.debug("Main Loop " + str(loops))

            # Make sure our rotary threads are alive and happy
            rotary1_thread = check_thread(rotary1_thread, rotary1_settings, logger)
            rotary2_thread = check_thread(rotary2_thread, rotary2_settings, logger)
            rotary3_thread = check_thread(rotary3_thread, rotary3_settings, logger)

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


if __name__ == '__main__':
    main()
