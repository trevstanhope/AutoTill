# AutoTill
## Formating SD
Download yyyy-mm-dd-wheezy-raspbian.img.
Unmount all partitions of the SD card:

    sudo umount /dev/mmcblk0p*
    
From the directory of the image file (this will take a while):

    dd bs=4M if=yyy-mm-dd-wheezy-raspbian.img of=/dev/mmcblk0
    
## First Boot
The first time the device is booted, it will prompt to set configurations.
This process can be repeated later with the command:

    raspi-config
    
When in the configuration editor, the following are ideal settings:
1. Keyboard layout? --> English US
2. Overclocking? --> Modest
3. 'pi' user password? --> 'password'
4. SSH? --> Enable
5. Desktop on Boot? --> Disable

## Installing Dependencies
Firstly, the entire set of repositories should be updated and upgraded.
(WARNING: This can take a while and requires an internet connection)

    sudo apt-get updatte && sudo apt-get upgrade
    
AutoTill requires Python 2.x, OpenCV, PIL and NumPy to process images:
 
    sudo apt-get install git-core python python-opencv python-numpy python-imaging

## Newest Code
The newest version of the AutoTill codebase can be acquired via git: 

    git clone https://github.com/trevstanhope/AutoTill.git
    
## Configuring Raspberry PI
1. Some faster USB cameras require adjusting module settings on the RaspberryPi.
If receiving timeout errors, move to the config/ directory and run:

    chmod +x TimeoutFix.sh
    ./TimeoutFix.sh
    
2. In most circumstances, the AutoTill system should be started on boot.
To enable (or disable) this functionality:

    sudo nano /etc/rc.local
    
You should now be in the nano text editor, add this line to the end of rc.local:

    sudo python /path/to/AutoTill.py ## enables AutoTill on boot
    
3. To allow for remote debugging of the AutoTill system, you may configure
a local ad-hoc network. First, the RaspberryPi needs to have a dhcp server:

    sudo apt-get install isc-dhcp-server
   
Then replace /etc/network/interfaces with the interfaces file in config/:

    sudo mv /etc/network/interfaces /etc/network/interfaces.backup
    sudo cp /home/pi/AutoTill/config/interfaces /etc/network/interfaces
    
Then replace /etc/dhcp/dhcpd.conf with dhcpd.conf in config/:

    sudo mv /etc/dhcp/dhcpd.conf /etc/dhcp/dhcpd.conf.backup
    sudo cp /home/pi/AutoTill/config/dhcpd.conf /etc/dhcp/dhcpd.conf

## Debugging
To connect to the AutoTill system's ad-hoc network, open an SSH client (PuTTY)
and connect to pi@192.168.1.1 with the password 'password'.
    
## Helping Commands
Kill AutoTill:

    sudo pkill python
    
List active processes:

    ps -e
