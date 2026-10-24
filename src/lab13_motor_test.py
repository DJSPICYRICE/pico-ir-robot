#******************************************************
# Lab 13 - PICO Project: Motor Test
# Authors: Mouli Grandhi and Michael Zimmerman
# Description: Cycles the robot through forward, reverse,
#              left and right to verify motor wiring.
#******************************************************

from machine import Pin
from time import sleep

# GPIO pins for the motor driver
LeftForward = 10
LeftBackward = 11
RightBackward = 12
RightForward = 13

lf = Pin(LeftForward, Pin.OUT)
lb = Pin(LeftBackward, Pin.OUT)
rf = Pin(RightForward, Pin.OUT)
rb = Pin(RightBackward, Pin.OUT)


def forward():
    lf.on()
    rf.on()
    lb.off()
    rb.off()


def backward():
    lb.on()
    rb.on()
    lf.off()
    rf.off()


def TurnRight():
    lf.on()
    rb.on()
    lb.off()
    rf.off()


def TurnLeft():
    lb.on()
    rf.on()
    lf.off()
    rb.off()


# Test loop
while True:
    forward()
    sleep(2)
    backward()
    sleep(2)
    TurnLeft()
    sleep(2)
    TurnRight()
    sleep(2)
