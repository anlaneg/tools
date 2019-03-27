#! /bin/bash

sudo rmmod altpciechdma
sudo insmod altpciechdma.ko
#sudo insmod prvpci.ko
dmesg
