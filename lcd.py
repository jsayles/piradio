"""
Info:
https://learn.adafruit.com/adafruit-led-backpack/bi-color-8x8-matrix-python-wiring-and-setup
https://github.com/adafruit/Adafruit_CircuitPython_HT16K33

Enable I2c:
sudo raspi-config
Interfacing Options -> I2C -> Enable

INSTALL:
sudo apt-get install python3-pip python3-pil i2c-tools
pip3 install adafruit-circuitpython-ht16k33

Find LCD:
sudo i2cdetect -y 1
"""

# Import all board pins and bus interface.
import board
import busio

# Import the HT16K33 LED matrix module.
from adafruit_ht16k33 import matrix


OFF = 0
GREEN = 1
RED = 2
ORANGE = 3

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# Create the matrix class.
display = matrix.Matrix8x8x2(i2c, address=0x70)

display.brightness = 1.0

# Clear the matrix.
display.fill(OFF)

# Set a pixel in the origin 0,0 position.
display[0, 0] = 1
# Set a pixel in the middle 8, 4 position.
display[8, 4] = 1
# Set a pixel in the opposite 15, 7 position.
display[15, 7] = 1
matrix.show()

# Change the brightness
matrix.brightness = 8

# Set the blink rate
matrix.blink_rate = 2
