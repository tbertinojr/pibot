import time
from time import sleep
import RPi.GPIO as GPIO
import curses
import sys, tty, termios
import gamepad
import Gamepad
from Gamepad import *
import os, struct, array
from fcntl import ioctl
from evdev import ecodes, InputDevice, ff, util, list_devices
import asyncio

def connect(): # asyncronus read-out of events
        xbox_path = None
        remote_control = 0 
        devices = [InputDevice(path) for path in list_devices()]
        print('Connecting to xbox controller...')
        for device in devices:
            if str.lower(device.name) == 'xbox wireless controller':
                xbox_path = str(device.path)
                remote_control = gamepad.gamepad(file = xbox_path)
                remote_control.rumble_effect = 2
                return remote_control
        return None

async def is_connected(): # asyncronus read-out of events
    path = None
    devices = [InputDevice(path) for path in list_devices()]
    for device in devices:
        if str.lower(device.name) == 'xbox wireless controller':
            path = str(device.path)
            print('Oh yeah')
    if(path == None):
        print('Xbox controller disconnected!!')
        return False
    return True
    await asyncio.sleep(5)

async def read_gamepad_inputs():
    print("Ready to drive!!")
    while is_connected():
        print("Still COnnected")
        await asyncio.sleep(30)
    return

def removetasks(loop):
    tasks = [t for t in asyncio.all_tasks() if t is not
             asyncio.current_task()]

    for task in tasks:
        # skipping over shielded coro still does not help
        if task._coro.__name__ == "cant_stop_me":
            continue
        task.cancel()

    print("Cancelling outstanding tasks")
##    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()

async def shutdown_signal(signal, loop):
    print(f"Received exit signal {signal.name}...")
    await removetasks(loop)

available()
connect()
sleep(0.5)

Gamepad()
loop = asyncio.get_event_loop()
loop.run_until_complete(is_connected())
asyncio.run(read_gamepad_inputs())
loop.close()
# 
 
