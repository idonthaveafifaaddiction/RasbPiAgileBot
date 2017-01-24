
from breezycreate2 import Robot
import logging
import time

logging.basicConfig(level=logging.DEBUG)

# Serial port constants
COMPORT_SIM = 'sim'

class RobotHandler:
    def init_bot(self, port):
        global robot
        robot = Robot()
        #robot = create.Create(port)
        logging.debug('robot created at port')

    def go(self, x, y):
        # Turn in place clockwise: -1
        # Turn in place counterclockwise: 1
        if y != 1 and y != -1:
            
            # Unless velocity is 0, trim to +/- limit
            if x != 0 and ( x > 100 or x < -100 ):
                x = x * (x/x)
            if y != 0 and ( y > 100 or y < -100 ): 
                y = y * (y/y)

            # velocity: A number between -500 and 500. Units are mm/s. 
            x = x * 5
            # radius: A number between -2000 and 2000. Units are mm.    
            y = y * 20 * -1 # Negate radius

            # Need some velocity to move when turning
            if x < 10 and x > -10 and y < 100:
                x = 200
                #y = 2 * (y/y)

            # If radius is very small, drive straight
            if y < 20 and y > -20:
                y = 32767 # Drive straight: 32767 (arbitrary number from breezy)

            print('x: ' + str(x) + ' y: ' + str(y))
            robot.drive(x, y) # drive(self, velocity, radius)
