import RPi.GPIO as GPIO 
from time import sleep

allGPIO_list = [3, 5, 7, 11, 13, 15]

Motor_A_EN = 7  # GPIO BORAD PIN 7
Motor_B_EN = 15  # GPIO BOARD PIN 15
Motor_A_1 = 3
Motor_A_2 = 5
Motor_B_1 = 11
Motor_B_2 = 13
pwm_a = None
pwm_b = None


def Motor_A_FWD():
    GPIO.output( 11, True )
    GPIO.output( 13, False )


def Motor_B_FWD():
    GPIO.output( 3, False )
    GPIO.output( 5, True )


def Motor_A_REV():
    GPIO.output( 13, True )
    GPIO.output( 11, False )


def Motor_B_REV():
    GPIO.output( 3, True )
    GPIO.output( 5, False )


def setup():  # Motor initialization
    global pwm_a, pwm_b
    GPIO.setwarnings( False )
    GPIO.setmode( GPIO.BOARD )
    GPIO.setup( Motor_A_EN, GPIO.OUT )
    GPIO.setup( Motor_B_EN, GPIO.OUT )
    GPIO.setup( Motor_A_1, GPIO.OUT )
    GPIO.setup( Motor_A_2, GPIO.OUT )
    GPIO.setup( Motor_B_1, GPIO.OUT )
    GPIO.setup( Motor_B_2, GPIO.OUT )

    try:
        pwm_a = GPIO.PWM( Motor_A_EN, 250 )  # Set Pin 7 to PWM / Set PWM freq
        pwm_b = GPIO.PWM( Motor_B_EN, 250 )  # Set Pin 15 to PWM / Set Freq
    except:
        pass


def forward():  # Forward Continuous
    Motor_A_FWD()
    Motor_B_FWD()
    speed()

def reverse():  # Reverse Continuous
    Motor_A_REV()
    Motor_B_REV()
    speed()

def left():  # Short Left Turn, Then Sleep
    Motor_A_REV()
    Motor_B_FWD()
    speed()
    sleep( 0.175 )
    stopAll()

def right():  # Short Right Turn, Then Sleep  
    Motor_A_FWD()
    Motor_B_REV()
    speed()
    sleep( 0.175 )
    stopAll()


def left_ninety():  # Turn Left 90 degrees
    Motor_A_REV()
    Motor_B_FWD()
    speed()
    sleep( 0.85 )
    stopAll()


def nineT_right():  # turn right 90 degrees
    Motor_A_FWD()
    Motor_B_REV()
    speed()
    sleep( 0.85 )
    stopAll()

def left_F():  # left Motor only forward
    Motor_A_FWD()
    speed()
    
def right_F():  # right Motor only forward
    Motor_B_FWD()
    speed()
    
def left_R():  # left Motor only forward
    Motor_A_REV()
    speed()
    
def right_R():  # right Motor only forward
    Motor_B_REV()
    speed()

def stopAll():
    GPIO.output( allGPIO_list, False )


def speed():
    pwm_a.ChangeDutyCycle( 100 )
    pwm_b.ChangeDutyCycle( 75 )
    
#PWM Enabled @ 0%

def pwm_start():
    pwm_a.start( 0 )
    pwm_b.start( 0 )
    GPIO.output( Motor_A_EN, True )
    GPIO.output( Motor_B_EN, True )
