#!/usr/bin/python
import time
from time import sleep
import RPi.GPIO as GPIO
import curses
import sys, tty, termios, time
import gamepad

class _Getch:
    """Gets a single character from standard input.
    Does not echo to the
    screen."""
    def __init__(self):
        self.impl = _GetchUnix()
    def __call__(self): return self.impl()

class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch





GPIO.setmode(GPIO.BOARD)

# This is the First Motor Output
GPIO.setup(03, GPIO.OUT)
# Forward Trigger
GPIO.setup(05, GPIO.OUT)
# Reverse Trigger
GPIO.setup(07, GPIO.OUT)
# Enable/PWM

# Second Motor Output
GPIO.setup(11, GPIO.OUT) # Forward Trigger
GPIO.setup(13, GPIO.OUT) # Reverse Trigger
GPIO.setup(15, GPIO.OUT) # Enable/ PWM Generator

allGPIO_list = (03,05,07,11,13,15)


def forward(x):
    GPIO.output(05, True)
    GPIO.output(03, False)
    GPIO.output(11, True)
    GPIO.output(13, False)
    pwm.ChangeDutyCycle(100)
    pwm1.ChangeDutyCycle(80)
    sleep(x)
"""
def forward(x, y):
    GPIO.output(05, True)
    GPIO.output(03, False)
    GPIO.output(11, True)
    GPIO.output(13, False)
    rampUp(y)
    sleep(x)
"""
def  reverse(x):
    
    GPIO.output(03, True)
    GPIO.output(05, False)
    GPIO.output(13, True)
    GPIO.output(11, False)
    pwm.ChangeDutyCycle(100)
    pwm1.ChangeDutyCycle(80)
    sleep(x)

def left():
    GPIO.output(05, True)
    GPIO.output(03, False)
    GPIO.output(13, True)
    GPIO.output(11, False)
    pwm.ChangeDutyCycle(100)
    pwm1.ChangeDutyCycle(100)
    sleep(0.35)
    GPIO.output(allGPIO_list, False) 
    

def right():
    GPIO.output(03, True)
    GPIO.output(05, False)
    GPIO.output(11, True)
    GPIO.output(13, False)
    pwm.ChangeDutyCycle(100)
    pwm1.ChangeDutyCycle(100)
    sleep(0.35)
    GPIO.output(allGPIO_list, False)
    
def stopAll():
    pwm.ChangeDutyCycle(0)
    pwm1.ChangeDutyCycle(0)
    GPIO.output(allGPIO_list, False) 

def speed(x):
    pwm.ChangeDutyCycle(x)
    pwm1.ChangeDutyCycle(x)
    return speed(x)
"""
def rampUp(speed):
    for x in range(10, speed):
        pwm.ChangeDutyCycle(x)
        pwm1.ChangeDutyCycle(x)
        sleep(0.025)
"""        
"""def rampDown(speed):
    z=speed
    for x in range(z,-1, -1):
        pwm.ChangeDutyCycle(x)
        print x
        sleep(0.015)
     """   
#Set PWM Pin Outs To pin 07, 15/set pwm freq

pwm=GPIO.PWM(07, 200)
pwm1=GPIO.PWM(15, 200)

# PWM Enabled @ 0%
pwm.start(0)
pwm1.start(0)

getch = _Getch()

#Forward Direction


GPIO.output(07, True)
GPIO.output(15, True)


def drive_motor(direction, speed):    
    if direction == "forward":
        forward(5,100)
    elif direction == "backward":
        reverse(5,100)
    else:
        stopAll()

def connect(): # asyncronus read-out of events
        xbox_path = None
        remote_control = None
        devices = [InputDevice(path) for path in list_devices()]
        print('Connecting to xbox controller...')
        for device in devices:
            if str.lower(device.name) == 'xbox wireless controller':
                xbox_path = str(device.path)
                remote_control = gamepad.gamepad(file = xbox_path)
                remote_control.rumble_effect = 2
                return remote_control
        return None

def is_connected(): # asyncronus read-out of events
    path = None
    devices = [InputDevice(path) for path in list_devices()]
    for device in devices:
        if str.lower(device.name) == 'xbox wireless controller':
            path = str(device.path)
    if(path == None):
        print('Xbox controller disconnected!!')
        return False
    return True

screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)

try:
        while True:
            char = screen.getch()
            if char == ord('q'):
                break
            elif char == curses.KEY_UP:
                forward(0.05)
            elif char == curses.KEY_DOWN:
                reverse(0.05)
            elif char == curses.KEY_RIGHT:
               right()
            elif char == curses.KEY_LEFT:
                left()
            elif char == ord('l'):
                stopAll()
finally:
    #Close down curses properly, inc turn echo back on!
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()
    GPIO.cleanup()









