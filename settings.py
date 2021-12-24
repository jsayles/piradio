LOG = "piradio.log"
DEBUG = False

ROTARY1_APin = 22
ROTARY1_BPin = 27
ROTARY1_SPin = 17

ROTARY2_APin = 23
ROTARY2_BPin = 24
ROTARY2_SPin = 18

ROTARY3_APin = 8
ROTARY3_BPin = 7
ROTARY3_SPin = 25

import os, sys
sys.path.append(os.environ['HOME'])

# Now get the local settings
from local_settings import *
