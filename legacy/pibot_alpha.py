#!/usr/bin/python

import PiMotor
import time
import RPi.GPIO as GPIO
import curses
import sys, tty, termios, time



m1 = PiMotor.Motor("MOTOR1",1)
m2 = PiMotor.Motor("MOTOR2",1)
m3 = PiMotor.Motor("MOTOR3",1)
m4 = PiMotor.Motor("MOTOR4",1)

allMotors = m1, m2, m3, m4

ab = PiMotor.Arrow(1)
al = PiMotor.Arrow(2)
af = PiMotor.Arrow(3)
ar = PiMotor.Arrow(4)

allLights = ab, af, al, ar

class _Getch:
    """Gets a single character from standard input.  Does not echo to the
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



timex = 0.02
for i in range(20):
    ab.on()
    time.sleep(timex)
    ab.off()
    time.sleep(timex)
    al.on()
    time.sleep(timex)
    al.off()
    time.sleep(timex)
    af.on()
    time.sleep(timex)
    af.off()
    time.sleep(timex)
    ar.on()
    time.sleep(timex)
    ar.off()
    time.sleep(timex)

getch = _Getch()

# Get the curses window, turn off echoing of keyboard to screen, turn on
# instant (no waiting) key response, and use special values for cursor keys
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
                af.on()
                ab.off()
                al.off()
                ar.off()
                m2.forward(50)
                m4.forward(80)
            elif char == curses.KEY_DOWN:
                ab.on()
                al.off()
                ar.off()
                af.off()
                m2.reverse(50)
                m4.reverse(50)
            elif char == curses.KEY_RIGHT:
                ar.on()
                al.off()
                ab.off()
                af.off()
                m2.reverse(50)
                m4.forward(50)
            elif char == curses.KEY_LEFT:
                al.on()
                ab.off()
                ar.off()
                af.off()
                m4.reverse(50)
                m2.forward(50)
            elif char == ord('l'):
                al.off()
                ab.off()
                ar.off()
                af.off()
                m4.stop()
                m2.stop()
finally:
    #Close down curses properly, inc turn echo back on!
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()
    GPIO.cleanup()








