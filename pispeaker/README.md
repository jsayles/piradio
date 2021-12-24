# Pi Speaker (Spotify)

## Hardware

https://learn.adafruit.com/adafruit-20w-stereo-audio-amplifier-class-d-max9744/overview

## Tutorials

https://learn.adafruit.com/adafruit-20w-stereo-audio-amplifier-class-d-max9744/python-circuitpython
https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1
https://github.com/adafruit/Adafruit_CircuitPython_MAX9744

## Install Raspotify

https://github.com/dtcooper/raspotify

## Allow non-root user to use GPIO and I2C

```
sudo groupadd i2c
sudo chown :i2c /dev/i2c-1
sudo chmod g+rw /dev/i2c-1
sudo usermod -a -G i2c jacob
sudo usermod -a -G gpio jacob
```

## Setup Max9744 Amp

Don't forget to enable I2C!

```
mkdir pispeaker && cd pispeaker
python3 -m venv .env
source .env/bin/activate
pip3 install adafruit-circuitpython-max9744
```
