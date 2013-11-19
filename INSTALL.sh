#!/bin/sh
# Install AutoTill
# Author: Trevor Stanhope
# NOTE: Must be executed from root directory of AutoTill/

# Dependencies
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install python python-opencv python-numpy python-imaging -y
sudo apt-get install isc-dhcp-server git-core -y

# Fix 'select timeout' error
sudo rmmod uvcvideo
sudo modprobe uvcvideo nodrop=1 timeout=5000 quirks=0x80

# Configure DHCP
sudo mv /etc/network/interfaces /etc/network/interfaces.backup
sudo cp config/interfaces /etc/network/interfaces
sudo mv /etc/dhcp/dhcpd.conf /etc/dhcp/dhcpd.conf.backup
sudo cp config/dhcpd.conf /etc/dhcp/dhcpd.conf

# Start on boot
sudo mv /etc/rc.local /etc/rc.local.backup
sudo cp config/rc.local /etc/rc.local
sudo chmod +x /etc/rc.local
sudo cp code/AutoTill.py /usr/bin/AutoTill.py
sudo chmod +x /usr/bin/AutoTill.py

