import board
import busio
import adafruit_max9744

board.SCL = 3
board.SDA = 2
i2c = busio.I2C(board.SCL, board.SDA)

amp = adafruit_max9744.MAX9744(i2c)
amp.volume = 31
