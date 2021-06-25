# Welcome to Berta voice assistant!
## Bachelor thesis: Development and evalution of a voice assistant system based on open source compoments.

Berta is a Raspberry Pi local voice assistant system based on open
source components.

See the following instructions on how to work with it.

Deployement on Linux or Raspberry Pi Hosting.
Raspberry Pi with Raspbian, official distribution from the Raspberry Pi Foundation.
Use a fresh setup SD Card with Raspbian for using Berta.

Installing Berta on Raspberry Pi by cloning the application directly from its git repository:
```
$ git clone https://github.com/PassionPlus/berta.git
```

after cloning berta, please run the install script as root (sudo will do)
```
$ ./install.sh
```

## Note:
all dependencies are located in a folder during installation named bertaDependancies (installed to the pi users home directory). If for any reason the installation fails, or berta cannot be started, in most cases the the daughter board drivers did not install correctly. To troubleshoot, please try the following steps:

- Restart the raspberry and try starting berta again
- if it still fails, rerun the following scripts found inside the bertaDependancies folder:
	- cd path/to/bertaDependancies
	- ./seeed-voicecard/ubuntu-prerequisite.sh
	- ./seeed-voicecard/install.sh

after another reboot, berta should be up and running


Helpfull Links:
Learn Python:
It's a Python 2 tutorial, but for the 
overview it's enough. 
https://developers.google.com/edu/python

Learn Flask:
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world


DeepSpeech:
https://deepspeech.readthedocs.io/en/r0.9/
https://www.hackster.io/dmitrywat/offline-speech-recognition-on-raspberry-pi-4-with-respeaker-c537e7
