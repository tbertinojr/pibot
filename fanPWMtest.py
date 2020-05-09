import RPi.GPIO as GPIO
from time import sleep
import curses
import sys, tty, termios  #Unsure as to what is actually needed

GPIO.setmode(GPIO.BOARD)

# This is the First Motor Output
GPIO.setup(03, GPIO.OUT) #Forward Trigger
GPIO.setup(05, GPIO.OUT) #Reverse Trigger
GPIO.setup(07, GPIO.OUT) #Enable/PWM

#Second Motor Output
GPIO.setup(11, GPIO.OUT) #Forward Trigger
GPIO.setup(13, GPIO.OUT) #Reverse Trigger
GPIO.setup(15, GPIO.OUT) #Enable/ PWM Generator

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
def  reverse(x,y):
    
    GPIO.output(03, True)
    GPIO.output(05, False)
    GPIO.output(13, True)
    GPIO.output(11, False)
    rampUp(y)
    sleep(x)
    
def right():
    GPIO.output(05, True)
    GPIO.output(03, False)
    GPIO.output(13, True)
    GPIO.output(11, False)
    pwm.ChangeDutyCycle(100)
    pwm1.ChangeDutyCycle(100)
    sleep(2.8)
    GPIO.output(allGPIO_list, False) 
    

def left():
    GPIO.output(03, True)
    GPIO.output(05, False)
    GPIO.output(11, True)
    GPIO.output(13, False)
    pwm.ChangeDutyCycle(100)
    pwm1.ChangeDutyCycle(100)
    sleep(2.8)
    GPIO.output(allGPIO_list, False) 
     
def stopAll():
    """
    for x in range(100,-1, -1):
        pwm.ChangeDutyCycle(x)
        pwm1.ChangeDutyCycle(x)
        print x
        sleep(0.015)
    """
    GPIO.output(allGPIO_list, False) 

def speed(x):
    pwm.ChangeDutyCycle(x)
    pwm1.ChangeDutyCycle(x)
    return speed(x)

def rampUp(speed):
    for x in range(10, speed):
        pwm.ChangeDutyCycle(x)
        pwm1.ChangeDutyCycle(x)
        print x
        sleep(0.025)
        
"""def rampDown(speed):
    z=speed
    for x in range(z,-1, -1):
        pwm.ChangeDutyCycle(x)
        print x
        sleep(0.015)
     """   
#Set PWM Pin Outs To pin 07, 15/set pwm freq

pwm=GPIO.PWM(07, 300)
pwm1=GPIO.PWM(15, 300)

# PWM Enabled @ 0%
pwm.start(0)
pwm1.start(0)

#Forward Direction
GPIO.output(07, True)
GPIO.output(15, True)
forward(1)
stopAll()

sleep(0.25)
reverse(1,101)
stopAll()

GPIO.output(07, True)
GPIO.output(15, True)

x=1
for x in range(0,2):
    left()
    sleep(0.25)
    right()
    sleep(0.25)

stopAll()

#Shutdown Enable Pin
#stopAll()
print "Cease All Motor Functions"

pwm.stop()
pwm1.stop()
GPIO.cleanup()
