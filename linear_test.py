#!/usr/bin/python


import time
import RPi.GPIO as GPIO

# ===========================================================================
# Example Code
# ===========================================================================

# L298N setup code

# Define Outputs to L298N 
en = 7
in1 = 35
in2 = 31
inpsec = 1.86 #2
# enB =
# in3 =
# in4 =

desireddistance = 2

calctime = desireddistance/inpsec

def up():
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)

def down():
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)

#GPIO.cleanup()

GPIO.setmode(GPIO.BOARD)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)

GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(en, GPIO.HIGH)


down()
time.sleep(calctime)

print (calctime)

GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)

GPIO.output(en, GPIO.LOW)

GPIO.cleanup()
