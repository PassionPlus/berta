#!/bin/bash

# This is the prerequisite script
# TODO More info
# TODO 

# ensure user is running as root
if [ "$EUID" -ne 0 ]
then 
	echo "ERROR: Script must be run as root. Exiting..."
	exit
fi


echo "******************************************************************"
echo "* Initializing system and dependencies for berta voice assistant *"
echo "******************************************************************"
echo ""
sleep 1

#check if non-free repo is not installed
if ! grep -E -q "debian.*non-free" /etc/apt/sources.list; 
then
    # add non-free packages to apt 
    echo "adding non-free packages to apt for dependancies..."
    wget -q https://ftp-master.debian.org/keys/release-10.asc -O- | apt-key add -
    echo "deb http://deb.debian.org/debian buster non-free" | tee -a /etc/apt/sources.list
    echo "DONE"
else
    echo "repo already added...skipping"
fi

sleep 1

echo "Updating and installing latest packages...."

# Update and upgrade raspberry
apt update && apt upgrade -y

echo "DONE"
echo "Installing needed OS dependancies"

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

git clone https://github.com/HinTak/seeed-voicecard.git #fixed seeed-voicecard driver
git clone https://github.com/mozilla/DeepSpeech-examples.git #Deepspeech examples; needed?
# git clone deepspeech?
curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.tflite
curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.pbmm
curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer
# clone deepspeech stuff
# clone 


# TODO Set up python environment
#cd /home/pi/berta

# *** OBSOLETE; see requirements.txt
#pip3 install virtualenv deepspeech flask uwsgi pvporcupine~=1.8.7 pyaudio~=0.2.11 webrtcvad~=2.0.10 halo~=0.0.18 numpy~=1.16.2 scipy~=1.5.4 soundfile


#reboot now

echo "**********"
echo "Done with first step, please reboot"
echo "**********"

# Create file to indicate we have finished the first part
# creating file in /var/tmp as it persists over reboots
# if user doesn't execute second script for some reason
# file will be deleted after OS Specific time (default = 30 days)
touch /var/tmp/firstStep.done
