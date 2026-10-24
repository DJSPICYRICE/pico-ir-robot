#******************************************************
# Lab 14 - PICO Project: IR Remote Control
# Authors: Mouli Grandhi and Michael Zimmerman
# Description: Drives the robot with an NEC IR remote.
#              PWM duty cycles balance the two motors.
#******************************************************

from machine import Pin, PWM
from ir_rx.nec import NEC_8
import utime

#--------------------------------------------------
# Pins
IRPinNum = 20
LeftForward = 10
LeftBackward = 11
RightBackward = 12
RightForward = 13

ir_pin = Pin(IRPinNum, Pin.IN, Pin.PULL_UP)
lf = PWM(Pin(LeftForward, Pin.OUT))
lf.freq(1000)
lb = PWM(Pin(LeftBackward, Pin.OUT))
lb.freq(1000)
rf = PWM(Pin(RightForward, Pin.OUT))
rf.freq(1000)
rb = PWM(Pin(RightBackward, Pin.OUT))
rb.freq(1000)

#--------------------------------------------------
# Movement functions
def forward():
    lf.duty_u16(64500)
    rf.duty_u16(65535)
    lb.duty_u16(0)
    rb.duty_u16(0)


def backward():
    lb.duty_u16(64500)
    rb.duty_u16(65535)
    lf.duty_u16(0)
    rf.duty_u16(0)


def TurnRight():
    lf.duty_u16(53000)
    rb.duty_u16(0)
    lb.duty_u16(0)
    rf.duty_u16(0)


def TurnLeft():
    lb.duty_u16(0)
    rf.duty_u16(53000)
    lf.duty_u16(0)
    rb.duty_u16(0)


def stop():
    lf.duty_u16(0)
    rb.duty_u16(0)
    lb.duty_u16(0)
    rf.duty_u16(0)

#--------------------------------------------------
# Map IR remote codes to movement functions
def controller(code):
    if code == 0x18:    # Up
        forward()
    elif code == 0x52:  # Down
        backward()
    elif code == 0x08:  # Left
        TurnLeft()
    elif code == 0x5A:  # Right
        TurnRight()
    elif code == 0x1C:  # OK
        stop()


def callback(data, addr, ctrl):
    controller(data)


# IR decoding runs in the background via interrupts
ir = NEC_8(ir_pin, callback)

#--------------------------------------------------
try:
    while True:
        utime.sleep(0.5)
except KeyboardInterrupt:
    stop()
