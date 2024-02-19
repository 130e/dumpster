#!/bin/sh
TIME=$(date +%Y-%m-%d-%H%M%S)
PORT=5257
SERVERIP=138.68.49.206
BANDWIDTH=0
DURATION=60
server() {
  iperf3 -s -p ${PORT} -J --logfile iperf-server-${TIME}-$1.log -1
}
prog2() {
  tcpdump -i eth0 port ${PORT} -w pcap-iperf-server-${TIME}-$1.pcap
}
udp_dev() {
  ./iperf3.9 -c ${SERVERIP} -uR -b ${BANDWIDTH} -i 0.1 -p ${PORT} -t ${DURATION} -J --logfile iperf-dev-${TIME}-$1.log
}

#prog1 & prog2 ; fg
#(trap 'kill 0' SIGINT; prog1 & prog2 & prog3)
udp_dev $1
