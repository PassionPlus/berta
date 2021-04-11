#!/bin/bash

# This is the prerequisite script
# TODO More info

# ensure user is running as root
if [ "$EUID" -ne 0 ]
	then echo "ERROR: Script must be run as root. Exiting..."
	exit
fi

echo "Test, running as root"

# Update and upgrade raspberry
apt update && apt upgrade -y

# install needed programms and dependancies
apt install -y git python3 nginx python3-pyaudio

mkdir -p /home/pi/bertaDependencies
cd /home/pi/bertaDependencies

# TODO git stuff
# clone forked and updated respeaker drivers
git clone https://github.com/HinTak/seeed-voicecard.git
# clone deepspeech stuff
# clone 


# TODO Download microphone script
# TODO Run microphone script
# TODO Set up python environment
# TODO ... Profit$?

#reboot now
