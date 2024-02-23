#!/bin/bash

TC=/sbin/tc

# interface traffic will leave on
IF=ens160

# The parent limit, children can borrow from this amount of bandwidth
# based on what's available.
LIMIT=100mbit

# the rate each child should start at
START_RATE=5mbit

# the max rate each child should get to, if there is bandwidth
# to borrow from the parent.
# e.g. if parent is limited to 100mbits, both children, if transmitting at max at the same time,
# would be limited to 50mbits each.
CHILD_LIMIT=80mbit

# host 1
DST_CIDR=192.168.5.0/32
# host 2
DST_CIDR_2=192.168.5.1/32

# filter command -- add ip dst match at the end
U32="$TC filter add dev $IF protocol ip parent 1:0 prio 1 u32"

create () {
  echo "== SHAPING INIT =="

  # create the root qdisc
  $TC qdisc add dev $IF root handle 1:0 htb \
    default 30

  # create the parent qdisc, children will borrow bandwidth from
  $TC class add dev $IF parent 1:0 classid \
    1:1 htb rate $LIMIT

  # create children qdiscs; reference parent
  $TC class add dev $IF parent 1:1 classid \
    1:10 htb rate $START_RATE ceil $CHILD_LIMIT
  $TC class add dev $IF parent 1:1 classid \
    1:30 htb rate $START_RATE ceil $CHILD_LIMIT

  # setup filters to ensure packets are enqueued to the correct
  # child based on the dst IP of the packet
  $U32 match ip dst $DST_CIDR flowid 1:10
  $U32 match ip dst $DST_CIDR_2 flowid 1:30

  echo "== SHAPING DONE =="
}

# run clean to ensure existing tc is not configured
clean () {
  echo "== CLEAN INIT =="
  $TC qdisc del dev $IF root
  echo "== CLEAN DONE =="
}

clean
create
