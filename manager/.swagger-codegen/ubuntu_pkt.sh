#!/usr/bin/env bash
#title           : ubuntu_pkt.sh
#description     : This script will configure container docker and VM env with th required pkg.
#author	     : HAMZA SAFRI
#date            : 20190806
#version         : 1
#usage	     : bash ubuntu_pkt.sh
#notes           : run this script before running python Monitoring Manager script
#bash_version    : 4.4.12(1)-release
#==============================================================================

today=$(date)


/usr/bin/clear
echo "     ================ $today ================   "



cyan='\e[0;36m'
green='\e[0;32m'
lightgreen='\e[0;32m'
white='\e[0;37m'
red='\e[0;31m'
yellow='\e[0;33m'
blue='\e[0;34m'
purple='\e[0;35m'
orange='\e[38;5;166m'
path=`pwd`


if [ $(id -u) != "0" ]; then
echo -e $red [x]::[not root]: You need to be [root] to run this script.$white;
      echo ""
   	  sleep 1
exit 0
fi

which pip> /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] pip......................[ found ]" $white
sleep 1
else
echo -e $red "[ X ] pip  -> not found" $white
apt-get install python-pip
fi

which python > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] python....................[ found ]" $white
sleep 1
else
echo -e $red "[ X ] python  -> not found" $white
apt install python
fi

which lsof > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] lsof....................[ found ]" $white
sleep 1
else
echo -e $red "[ X ] lsof  -> not found" $white
apt install lsof
fi

which screen > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] screen....................[ found ]" $white
sleep 1
else
echo -e $red "[ X ] screen  -> not found" $white
apt install screen
fi

which iostat > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] sysstat....................[ found ]" $white
sleep 1
else
echo -e $red "[ X ] sysstat  -> not found" $white
apt install sysstat
fi

which ifstat > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] ifstat....................[ found ]" $white
sleep 1
else
echo -e $red "[ X ] ifstat  -> not found" $white
apt install ifstat
fi

which ssh > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e $green "[ ✔ ] ssh....................[ found ]" $white
sleep 1
else
echo -e $red "[ X ] ssh  -> not found" $white
apt install ssh
sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
/etc/init.d/ssh restart
fi
