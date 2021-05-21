#!/bin/bash

# This is the prerequisite script
# TODO More info
# TODO jkhdfajklfhdjkslfhjdksla

# ensure user is running as root
if [ "$EUID" -ne 0 ]
	then echo "ERROR: Script must be run as root. Exiting..."
	exit
fi

echo "Test, running as root"

# add non-free packages to apt 
wget -q https://ftp-master.debian.org/keys/release-10.asc -O- | apt-key add -
echo "deb http://deb.debian.org/debian buster non-free" | tee -a /etc/apt/sources.list

# Update and upgrade raspberry
apt update && apt upgrade -y

# install needed programms and dependancies
# to fix numpy, libatlas-base-dev is needed
apt install -y git build-essential python3 python3-dev nginx python3-pyaudio libatlas-base-dev libttspico-utils

# TODO set up nginx, and flask project
#service nginx start

mkdir -p /home/pi/bertaDependencies
#mkdir -p /home/pi/berta

#chwon www-data /home/pi/berta

cd /home/pi/bertaDependencies

# TODO git stuff
# clone forked and updated respeaker drivers
git clone https://github.com/HinTak/seeed-voicecard.git
git clone https://github.com/mozilla/DeepSpeech-examples.git
curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.tflite
curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.pbmm
curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer
# clone deepspeech stuff
# clone 

# TODO Set up python environment
cd /home/pi/berta

pip3 install virtualenv deepspeech flask uwsgi pvporcupine~=1.8.7 pyaudio~=0.2.11 webrtcvad~=2.0.10 halo~=0.0.18 numpy~=1.16.2 scipy~=1.5.4 soundfile

# TODO create requirements.txt


#reboot now

echo "**********"
echo "Done with first step, please reboot"
echo "**********"

