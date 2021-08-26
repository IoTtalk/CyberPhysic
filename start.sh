#!/bin/sh
#create a new screen session in detached mode
screen -d -m -S CyberPhysic
screen -X screen -t "CyberPhysic" bash -c "sudo python3 cyberphysic.py"
screen -X screen -t "Line_notify" bash -c "sudo python3 line_notify.py"