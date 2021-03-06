# Pi Radio
Pi based Internet Radio

For a list of stations see [stations.md](stations.md)

## Pi Setup

Start with Raspian Stretch

### Basics
```
sudo apt-get install tux git python3-pip
```

### Music Player Daemon
```
sudo apt-get install mid mpc
```

### Bluetooth speaker
```
sudo apt-get install pi-bluetooth
sudo apt-get install blueman pulseaudio pavucontrol pulseaudio-module-bluetooth  
```

### Force audio over 3.5mm jack
```
sudo echo "audio_pwm_mode=2" | sudo tee -a /boot/config.txt
```

### Sonos Control ###
http://docs.python-soco.com/en/latest/

### Set volume to 85%
```
sudo amixer set PCM -- 85%
```

## Setup Tutorials

### Pi3 as Bluetooth Speaker Setup
https://www.raspberrypi.org/forums/viewtopic.php?t=161944
https://github.com/davidedg/NAS-mod-config/blob/master/bt-sound/bt-sound-Bluez5_PulseAudio5.txt
http://markus.jarvisalo.dy.fi/2017/12/making-the-raspberry-pi-3-a-bluetooth-audio-receiver/

## Hardware

LCD Hole:  27mm x 34mm max

## MAX 9744 Amp Tutorial

https://github.com/adafruit/Adafruit_Python_MAX9744

### Monocrome LCD
https://www.adafruit.com/product/938
https://learn.adafruit.com/ssd1306-oled-displays-with-raspberry-pi-and-beaglebone-black/overview

### Touchscreen Radio Tutorial
https://learn.adafruit.com/raspberry-pi-radio-player-with-touchscreen/installing-the-music-player-daemon
