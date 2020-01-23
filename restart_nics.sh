#!/bin/bash

ifdown wlan0
ifdown eth0

sleep 10

ifup wlan0
ifup eth0
