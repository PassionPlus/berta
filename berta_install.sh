#!/bin/bash

# this is the second script

# ensure user is running as root
if [ "$EUID" -ne 0 ]
then
    echo "ERROR: Script must be run as root. Exiting..."
    exit
# ensure that run_me_first script was already run
elif [ ! -f "/var/tmp/firstStep.done" ]
then
    echo "ERROR: probably didn't run initial script. Exiting..."
    exit
fi

echo "Doing some stuff"

# run driver script

# ubuntu substitutes sh to dash, we want bash
bash /home/pi/bertaDependencies/seeed-voicecard/install.sh




# clean up
rm /var/tmp/firstStep.done
