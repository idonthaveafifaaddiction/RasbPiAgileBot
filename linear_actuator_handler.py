import time

gpio_available = False

try:
    import RPi.GPIO as GPIO
    gpio_available = True
except ImportError:
    pass


in1 = 35
in2 = 33


class LinearActuatorHandler:
    def init_linear_actuator(self):
        if gpio_available:
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(in1,GPIO.OUT)
            GPIO.setup(in2,GPIO.OUT)
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.LOW)

    
    def stop(self):
        if gpio_available:
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.LOW)
        
    def up(self):
        if gpio_available:
            GPIO.output(in1,GPIO.HIGH)
            GPIO.output(in2,GPIO.LOW)
 
    def down(self):
        if gpio_available:
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.HIGH)
