#!/bin/sh
TIME=$(date +%Y-%m-%d-%H%M%S)
PORT=5252
prog1() {
  iperf3 -s -p ${PORT} -J --logfile iperf-server-${TIME}.log
}
prog2() {
  tcpdump -i ens3 port ${PORT} -C 1000 -w pcap-iperf-server-${TIME}
}

prog1 & prog2 ; fg
#(trap 'kill 0' SIGINT; prog1 & prog2 & prog3)
