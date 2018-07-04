#! /bin/bash

sudo rmmod altpciechdma
sudo insmod altpciechdma.ko
dmesg
