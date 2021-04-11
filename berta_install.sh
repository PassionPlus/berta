#!/bin/bash

# This is the install script
# TODO More info

# ensure user is running as root
if [ "$EUID" -ne 0 ]
	then echo "ERROR: Script must be run as root. Exiting..."
	exit
fi

echo "Test, running as root"

# Update and upgrade raspberry
apt update && apt 


# TODO Download microphone script
# TODO Run microphone script
# TODO install needed programms and dependancies
# TODO Set up python environment
# TODO ... Profit$?
