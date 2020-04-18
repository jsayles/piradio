import os
import sys
import logging
import time
import threading
import traceback

import soco

import settings


logger = logging.getLogger('piradio')


def find_sonos():
    our_sonos = None
    if hasattr(settings, "SONOS_NAME"):
        logger.debug("Searching for '%s'..." % settings.SONOS_NAME)
        our_sonos = soco.discovery.by_name(settings.SONOS_NAME)
    else:
        # Name isn't set so return any sonos we find
        logger.debug("Searching for any Sonos speaker...")
        our_sonos = soco.discovery.any_soco()
    if not our_sonos:
        raise Exception("Could not find Sonos speaker!")

    ip = our_sonos.ip_address
    name = our_sonos.player_name
    model_name = our_sonos.get_speaker_info()['model_name']
    logger.info(f"Found a {model_name} named {name} at {ip}")

    return our_sonos


def get_fav_uri(sonos):
    # Grab the URI that is at the top of our favorites list
    uri = None
    favs = sonos.get_sonos_favorites()
    if 'favorites' in favs and len(favs) > 0:
        uri = favs['favorites'][0]['uri']
    return uri
