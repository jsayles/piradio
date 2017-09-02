from RPi import GPIO
from time import sleep

clk = 4
dt = 17

GPIO.setmode(GPIO.BCM)
#GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_UP)

counter = 0
clkLastState = GPIO.input(clk)

print "Starting up..."
try:

        while True:
                clkState = GPIO.input(clk)
                dtState = GPIO.input(dt)
                if clkState != clkLastState:
                        if dtState != clkState:
                                counter += 1
                        else:
                                counter -= 1
                        print counter
                clkLastState = clkState
                sleep(0.01)
finally:
        GPIO.cleanup()
