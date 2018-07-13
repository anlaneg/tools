#! /bin/bash

iptables -t nat -F PREROUTING
iptables -t nat -F POSTROUTING

iptables -t nat -A PREROUTING -d 8.8.8.8/32 -j DNAT --to-destination 10.160.34.7
iptables -t nat -A POSTROUTING -s 10.160.35.4/32  -j SNAT --to-source 9.9.9.9

#list
iptables -t nat -L
