#!/usr/bin/python3

import time
from time import sleep
from typing import Tuple
import RPi.GPIO as GPIO
import curses
import sys, tty, termios
sys.path.append( "/usr/lib/python3/dist-packages" )
sys.path.append( "/home/pi/pibot/pibot" )
import Gamepad as GP
import os, struct, array
from fcntl import ioctl
from evdev import ecodes, InputDevice, ff, util, list_devices
import asyncio
import getGetch
import gamepad
import signal
import pbot_setup


pbot = pbot_setup
pbot.setup()
pbot.pwm_start()



getch = getGetch._Getch()  #getch obj for recieving keyboard input


## FOR FUTURE XBOX ONE CONTROLLER CONNECTIVITY



###Testing Block#############

async def removetasks(loop):
    tasks = [t for t in asyncio.all_tasks() if t is not
             asyncio.current_task()]

    for task in tasks:
        # skipping over shielded coro still does not help
        if task._coro.__name__ == "cant_stop_me":
            continue
        task.cancel()

    print("Cancelling outstanding tasks")
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()

def connect_gamepad():  # asyncronus read-out of events
    xbox_path = None
    remote_control = None
    devices = [InputDevice(path) for path in list_devices()]
    print('Connecting to xbox controller...')
    for device in devices:
        if str.lower(device.name) == "xbox wireless controller":
            xbox_path = str(device.path)
            remote_control = gamepad.gamepad(file=xbox_path)
            remote_control.rumble_effect = 2
            return remote_control
    return None


def is_gamepad_connected():  # asyncronus read-out of events
    xbox_path = None
    devices = [InputDevice(path) for path in list_devices()]
    for device in devices:
        if str.lower(device.name) == "xbox wireless controller":
            xbox_path = str(device.path)
    if xbox_path is None:
        print("Xbox controller disconnected!!")
        return False
    return True


def update(old, new, max_delta=0.3):
    if abs(old - new) <= max_delta:
        res = new
    else:
        res = 0.0
    return res


async def read_gamepad_inputs():
    print("Ready to roooll!!")
    while  is_gamepad_connected():
        await asyncio.sleep(5e-3)
    return

remote_control = None
loop = asyncio.get_event_loop()
signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)

for s in signals:
    loop.add_signal_handler(s, lambda s=s: asyncio.create_task(shutdown_signal(s, loop)))
    try:
        remote_control = connect_gamepad()
        if remote_control is None:
            print('Please connect an Xbox controller then restart the program!')
            sys.exit()

        remote_control.rumble_effect = 2
        tasks = [remote_control.read_gamepad_input(), remote_control.rumble(), read_gamepad_inputs()]
        loop.run_until_complete(asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED))
        loop.run_until_complete(removetasks(loop))
    except:
        print('Exiting Program')
        sys.exit()
        GPIO.cleanup()
    finally:
        GPIO.cleanup()
#############################

screen = curses.initscr()
screen.keypad( True )

# DRIVE COMMANDS INPUT FROM KEYBOARD
try:
    while True:
        char = screen.getch()
        if char == ord( 'q' ):
            break
        elif char == curses.KEY_UP:
            pbot.forward()
        elif char == curses.KEY_DOWN:
            pbot.reverse()
        elif char == curses.KEY_RIGHT:
            pbot.right()
        elif char == curses.KEY_LEFT:
            pbot.left()
        elif char == ord( 'w' ):
            forward( 0.1 )
        elif char == ord( 's' ):
            reverse( 0.1 )
        elif char == ord( 'd' ):
            right()
        elif char == ord( 'a' ):
            left()
        elif char == ord( 'l' ):
            stopAll()
        elif char == ord( '1' ):
            left_ninety()
        elif char == ord( '2' ):
            nineT_right()
    
finally:
    # Close down curses properly,  turn echo back on!
    screen.keypad( 0 );
    curses.endwin()
    GPIO.cleanup()
    # END OF PROGRAM
