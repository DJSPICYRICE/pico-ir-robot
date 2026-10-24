#******************************************************
# Lab 15 - PICO Project: Final Robot
# Authors: Mouli Grandhi and Michael Zimmerman
# Description: IR remote-controlled robot with turn signals,
#              hazard lights, and ultrasonic collision stop.
#******************************************************

from machine import Pin, PWM
from ir_rx.nec import NEC_8
from hcsr04 import HCSR04
import utime

# dir: 0 = forward/stopped, 1 = left, 2 = right, 3 = reverse
dir = 0
distance = 100
forceStop = False

IRPinNum = 20
LeftForward = 10
LeftBackward = 11
RightBackward = 12
RightForward = 13

#--------------------------------------------------
# Pins
ir_pin = Pin(IRPinNum, Pin.IN, Pin.PULL_UP)
lf = PWM(Pin(LeftForward, Pin.OUT))
lf.freq(1000)
lb = PWM(Pin(LeftBackward, Pin.OUT))
lb.freq(1000)
rf = PWM(Pin(RightForward, Pin.OUT))
rf.freq(1000)
rb = PWM(Pin(RightBackward, Pin.OUT))
rb.freq(1000)

leftTurn = Pin(0, Pin.OUT)
leftStop = Pin(1, Pin.OUT)
rightTurn = Pin(2, Pin.OUT)
rightStop = Pin(4, Pin.OUT)

sensor = HCSR04(trigger_pin=6, echo_pin=7, echo_timeout_us=10000)

#--------------------------------------------------
def LEDoff():
    leftTurn.off()
    rightStop.off()
    leftStop.off()
    rightTurn.off()

#--------------------------------------------------
# Movement functions
def forward():
    global dir
    if forceStop:  # Too close to an obstacle: block forward and turns
        stop()
    else:
        lf.duty_u16(64500)
        rf.duty_u16(65535)
        lb.duty_u16(0)
        rb.duty_u16(0)
        dir = 0


def backward():
    global dir, forceStop
    lb.duty_u16(64500)
    rb.duty_u16(65535)
    lf.duty_u16(0)
    rf.duty_u16(0)
    dir = 3
    forceStop = False  # Reversing clears the obstacle flag


def TurnRight():
    global dir
    if forceStop:
        stop()
    else:
        lf.duty_u16(53000)
        rb.duty_u16(0)
        lb.duty_u16(0)
        rf.duty_u16(0)
        dir = 2


def TurnLeft():
    global dir
    if forceStop:
        stop()
    else:
        lb.duty_u16(0)
        rf.duty_u16(53000)
        lf.duty_u16(0)
        rb.duty_u16(0)
        dir = 1


def stop():
    global dir
    lf.duty_u16(0)
    rb.duty_u16(0)
    lb.duty_u16(0)
    rf.duty_u16(0)
    dir = 0

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
# Main loop: signal lights + obstacle check
try:
    while True:
        if dir == 0:
            LEDoff()
        elif dir == 1:  # Left turn signal
            leftTurn.on()
            utime.sleep(0.5)
            leftTurn.off()
            utime.sleep(0.5)
        elif dir == 2:  # Right turn signal
            rightTurn.on()
            utime.sleep(0.5)
            rightTurn.off()
            utime.sleep(0.5)
        elif dir == 3:  # Hazards while reversing
            rightStop.on()
            leftStop.on()
            utime.sleep(0.5)
            leftStop.off()
            rightStop.off()
            utime.sleep(0.5)

        distance = sensor.distance_cm()
        if 0 < distance < 10:
            stop()
            forceStop = True  # Obstacle within 10 cm

        utime.sleep(0.1)
except KeyboardInterrupt:
    stop()
