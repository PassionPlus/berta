#!/bin/bash

# This is the prerequisite script
# TODO TEMPLATE
# DONE Verify running as root
# DONE Verify correct Kernel version
# DONE Update system
# DONE Generate RSA Key
# DONE Supervisor stuff
# DONE move nginx config to correct folder (/etc/nginx/sites-enabled/berta)
# DONE Reload nginx service
# DONE set up python environment

# ************************
# * Step 1: REQUIREMENTS *
# ************************
REQ_MAJ=5
REQ_MIN=10

# * Ensure user is running as root *

if [ "$EUID" -ne 0 ]
then 
	echo "ERROR: Script must be run as root. Exiting..."
	exit 1
fi

# Check Kernel Version
KERNEL=$(uname -r)
MAJ=$(awk -F . '{print $1}' <<< $KERNEL)
MIN=$(awk -F . '{print $2}' <<< $KERNEL)

if [ "$MAJ" -lt "$REQ_MAJ" ] && [ "$MIN" -lt "$REQ_MIN" ]
then
    echo "ERROR: Kernel Version to low"
    echo "You're current Kernel version is: $KERNEL"
    echo "Please update to a Kernel verion: $REQ_MAJ.$REQ_MIN+"
    exit 1
fi

echo "******************************************************************"
echo "*                                                                *"
echo "* Initializing system and dependencies for berta voice assistant *"
echo "*                                                                *"
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

# *************************
# * Step 2: Update System *
# *************************
echo "Updating and installing latest packages...."

# Update and upgrade raspberry
apt update && apt upgrade -y

echo "DONE"
echo "Installing needed OS dependancies"

# install needed programms and dependancies
# to fix numpy, libatlas-base-dev is needed
apt install -y git openssl build-essential python3 python3-dev nginx python3-pyaudio libatlas-base-dev libttspico-utils supervisor

echo "DONE"

# ************************************
# * Step 3: Get further Dependencies *
# ************************************
mkdir -p /home/pi/bertaDependencies
cd /home/pi/bertaDependencies

echo "Downloading Deepspeech Model"
curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.tflite
mv deepspeech-*.tflite /home/pi/berta/app/libs

echo "Downloading Deepspeech scorer"
curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer
mv deepspeech-*.scorer /home/pi/berta/app/libs

# set up Respeaker card
echo "Setting up ReSpeaker daughter board"
git clone https://github.com/HinTak/seeed-voicecard.git #fixed seeed-voicecard driver
./seeed-voicecard/ubuntu-prerequisite.sh
./seeed-voicecard/install.sh

cd /home/pi/berta
# Don't delete dependancies, just in case
#rm -rf /home/pi/bertaDependencies

# *************************************
# * Step 4: Set up Python environment *
# *************************************

python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
deactivate

# **********************************************************
# * Step 5: Set up Supervisor to restart website if needed *
# **********************************************************

# If supervisor dir does not exists, create it
SUPERVISOR="/ect/supervisor/conf.d"
if [ ! -d "$SUPERVISOR" ]
then
	mkdir $SUPERVISOR
fi

cp /home/pi/berta/deployment/supervisor/berta.conf /etc/supervisor/conf.d/
supervisorctl reload

# *****************************************************
# * Step 6: Set up self signed certificates for NGINX *
# *****************************************************

echo "Creating self signed certificates"


domain=berta.de
commonname=$domain
country=DE
state=Ba-Wu
locality=MA
organization=Berta.de
organizationalunit=VoiceAssistant
email=berta@berta.de
password=dummypassword

openssl req -new -newkey rsa:4096 -days 365 -nodes -x509 -keyout key.pem -out cert.pem -subj "/C=$country/ST=$state/L=$locality/O=$organization/OU=$organizationunit/CN=$commonname/emailAddress=$email"

mkdir certs
mv key.pem ./certs/
mv cert.pem ./certs/

NGINX="/etc/nginx/sites-enabled"
if [ ! -d "$NGINX" ]
then
	mkdir $NGINX
else
	rm /etc/nginx/sites-enabled/default
fi

mv /home/pi/berta/deployment/nginx/berta /etc/sites-enabled/

service nginx reload

echo "**************************************************************"
echo "*                                                            *"
echo "* Done with setting up Berta, please reboot and run berta.sh *"
echo "*                                                            *"
echo "**********************************************************i***"

