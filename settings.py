LOG = "piradio.log"
DEBUG = False

ROTARY1_APin = 23
ROTARY1_BPin = 24
ROTARY1_SPin =  4

ROTARY2_APin = 27
ROTARY2_BPin = 22
ROTARY2_SPin = 25

import os, sys
sys.path.append(os.environ['HOME'])
sys.path.append('/home/pi')
# Now get the local settings
from local_settings import *
