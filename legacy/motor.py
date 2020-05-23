#!/usr/bin/python3

import time

import RPi.GPIO as GPIO



Motor_A_EN    = 7
Motor_B_EN    = 15

Motor_A_Pin1  = 3
Motor_A_Pin2  = 5
Motor_B_Pin1  = 11
Motor_B_Pin2  = 13

Dir_forward   = 0
Dir_backward  = 1

pwm_A = 0
pwm_B = 0

def setup():#Motor initialization
	global pwm_A, pwm_B
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(Motor_A_EN, GPIO.OUT)
	GPIO.setup(Motor_B_EN, GPIO.OUT)
	GPIO.setup(Motor_A_Pin1, GPIO.OUT)
	GPIO.setup(Motor_A_Pin2, GPIO.OUT)
	GPIO.setup(Motor_B_Pin1, GPIO.OUT)
	GPIO.setup(Motor_B_Pin2, GPIO.OUT)
	try:
		pwm_A = GPIO.PWM(Motor_A_EN, 250)
		pwm_B = GPIO.PWM(Motor_B_EN, 250)
	except:
		pass

def motorStop():#Motor stops
	GPIO.output(Motor_A_Pin1, GPIO.LOW)
	GPIO.output(Motor_A_Pin2, GPIO.LOW)
	GPIO.output(Motor_B_Pin1, GPIO.LOW)
	GPIO.output(Motor_B_Pin2, GPIO.LOW)
	GPIO.output(Motor_A_EN, GPIO.LOW)
	GPIO.output(Motor_B_EN, GPIO.LOW)

def motor_right(status, direction, speed):#Motor 2 positive and negative rotation
	global  pwm_B
	if status == 0: # stop
		motorStop()
	else:
		if direction == Dir_forward:
			GPIO.output(Motor_B_Pin1, GPIO.HIGH)
			GPIO.output(Motor_B_Pin2, GPIO.LOW)
			pwm_B.start(100)
			pwm_B.ChangeDutyCycle(speed)
		elif direction == Dir_backward:
			GPIO.output(Motor_B_Pin1, GPIO.LOW)
			GPIO.output(Motor_B_Pin2, GPIO.HIGH)
			pwm_B.start(0)
			pwm_B.ChangeDutyCycle(speed)
def motor_left(status, direction, speed):#Motor 1 positive and negative rotation
	global pwm_A
	if status == 0: # stop
		motorStop()
	else:
		if direction == Dir_forward:#
			GPIO.output(Motor_A_Pin1, GPIO.HIGH)
			GPIO.output(Motor_A_Pin2, GPIO.LOW)
			pwm_A.start(100)
			pwm_A.ChangeDutyCycle(speed)
		elif direction == Dir_backward:
			GPIO.output(Motor_A_Pin1, GPIO.LOW)
			GPIO.output(Motor_A_Pin2, GPIO.HIGH)
			pwm_A.start(0)
			pwm_A.ChangeDutyCycle(speed)
	return direction


def destroy():
	motorStop()
	#GPIO.cleanup()             # Release resource


try:
	pass
except KeyboardInterrupt:
	destroy()
