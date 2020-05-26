#!/usr/bin/python
import time
from time import sleep
import RPi.GPIO as GPIO
import curses
import sys, tty, termios

sys.path.append("/usr/lib/python3/dist-packages")
sys.path.append("/home/pi/pibot/pibot")
import gamepad
import os, struct, array
from fcntl import ioctl
from evdev import ecodes, InputDevice, ff, util
import asyncio
import getGetch

Motor_A_EN = 7  # GPIO BORAD PIN 7
Motor_B_EN = 15  # GPIO BOARD PIN 15
Motor_A_1 = 3
Motor_A_2 = 5
Motor_B_1 = 11
Motor_B_2 = 13
# Dir_forward   = 0
# Dir_backward  = 1
pwm_a = None
pwm_b = None

allGPIO_list = (3, 5, 7, 11, 13, 15)


def setup():  # Motor initialization
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(Motor_A_EN, GPIO.OUT)
    GPIO.setup(Motor_B_EN, GPIO.OUT)
    GPIO.setup(Motor_A_1, GPIO.OUT)
    GPIO.setup(Motor_A_2, GPIO.OUT)
    GPIO.setup(Motor_B_1, GPIO.OUT)
    GPIO.setup(Motor_B_2, GPIO.OUT)

    try:
        pwm_a = GPIO.PWM(Motor_A_EN, 250)  # Set Pin 7 to PWM / Set PWM freq
        pwm_b = GPIO.PWM(Motor_B_EN, 250)  # Set Pin 15 to PWM / Set Freq
    except:
        pass


def forward(x):  # Forward Continuous
    GPIO.output(5, True)
    GPIO.output(3, False)
    GPIO.output(11, True)
    GPIO.output(13, False)
    pwm_a.ChangeDutyCycle(100)  # pwm_a & pwm_b DIFFERENT CYCLES TO TRY AND MATCH SPEED
    pwm_b.ChangeDutyCycle(80)  # WOULD LIKE TO REPLACE CURRENT DC MOTORS WITH SERVO OR
    sleep(x)  # ADD ENCODER FOR SYNC FEEDBACK


def reverse(x):  # Reverse Continuous
    GPIO.output(3, True)
    GPIO.output(5, False)
    GPIO.output(13, True)
    GPIO.output(11, False)
    pwm_a.ChangeDutyCycle(100)
    pwm_b.ChangeDutyCycle(80)
    sleep(x)


def left():  # Short Left Turn, Then Sleep
    GPIO.output(5, True)
    GPIO.output(3, False)
    GPIO.output(13, True)
    GPIO.output(11, False)
    pwm_a.ChangeDutyCycle(100)
    pwm_b.ChangeDutyCycle(100)
    sleep(0.175)
    GPIO.output(allGPIO_list, False)


def right():  # Short Right Turn, Then Sleep
    GPIO.output(3, True)
    GPIO.output(5, False)
    GPIO.output(11, True)
    GPIO.output(13, False)
    pwm_a.ChangeDutyCycle(100)
    pwm_b.ChangeDutyCycle(100)
    sleep(0.175)
    stopAll()


def left_ninety():
    GPIO.output(5, True)
    GPIO.output(3, False)
    GPIO.output(13, True)
    GPIO.output(11, False)
    pwm_a.ChangeDutyCycle(100)
    pwm_b.ChangeDutyCycle(100)
    sleep(0.85)
    stopAll()


def nineT_right():
    GPIO.output(3, True)
    GPIO.output(5, False)
    GPIO.output(11, True)
    GPIO.output(13, False)
    pwm_a.ChangeDutyCycle(100)
    pwm_b.ChangeDutyCycle(100)
    sleep(0.85)
    stopAll()


def stopAll():
    pwm_a.ChangeDutyCycle(0)
    pwm_b.ChangeDutyCycle(0)
    GPIO.output(allGPIO_list, False)


def speed(x):
    pwm_a.ChangeDutyCycle(x)
    pwm_b.ChangeDutyCycle(x)
    return speed(x)


setup()
Gamepad.init()
# PWM Enabled @ 0%
pwm_a.start(0)
pwm_b.start(0)
GPIO.output(Motor_A_EN, True)
GPIO.output(Motor_B_EN, True)

getch = getGetch._Getch()


## FOR FUTURE XBOX ONE CONTROLLER CONNECTIVITY
def connect():  # asyncronus read-out of events
    xbox_path = None
    remote_control = None
    devices = [InputDevice(path) for path in list_devices()]
    print('Connecting to xbox controller...')
    for device in devices:
        if str.lower(device.name) == 'xbox wireless controller':
            xbox_path = str(device.path)
            remote_control = gamepad.gamepad(file=xbox_path)
            remote_control.rumble_effect = 2
            return remote_control
    return None


def is_connected():  # asyncronus read-out of events
    path = None
    devices = [InputDevice(path) for path in list_devices()]
    for device in devices:
        if str.lower(device.name) == 'xbox wireless controller':
            path = str(device.path)
    if (path == None):
        print('Xbox controller disconnected!!')
        return False
    return True


connect()

screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)

# DRIVE COMMANDS INPUT FROM KEYBOARD
try:
    while True:
        char = screen.getch()
        if char == ord('q'):
            break
        elif char == curses.KEY_UP:
            forward(0.1)
        elif char == curses.KEY_DOWN:
            reverse(0.1)
        elif char == curses.KEY_RIGHT:
            right()
        elif char == curses.KEY_LEFT:
            left()
        elif char == ord('w'):
            forward(0.1)
        elif char == ord('s'):
            reverse(0.1)
        elif char == ord('d'):
            right()
        elif char == ord('a'):
            left()
        elif char == ord('l'):
            stopAll()
        elif char == ord('1'):
            left_ninety()
        elif char == ord('2'):
            nineT_right()

finally:
    # Close down curses properly,  turn echo back on!
    curses.nocbreak()
    screen.keypad(0)
    curses.echo()
    curses.endwin()
    GPIO.cleanup()
    # END OF PROGRAM
