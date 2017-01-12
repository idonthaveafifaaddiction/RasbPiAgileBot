
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
        if y != 1 and y != -1 and x != 0:
            
            if x > 100 or x < -100:
                x = x * (x/x)
            if y > 100 or y < -100: 
                y = y * (y/y)

            #velocity: A number between -500 and 500. Units are mm/s. 
            x = x * 5
            #radius: A number between -2000 and 2000. Units are mm.    
            y = y * 200 * -1 # Negate radius

            # Need some velocity to move when turning
            # if x < 50 and x > -50 and y != 0:
            #     if x == 0:
            #         x = 50
            #     else:
            #         x = (x / x) * 50

            # If radius is very small, drive straight
            if y < 10 and y > -10:
                y = 32767 # Drive straight: 32767 (arbitrary number from breezy)

            # Radius should be between -2000 and 2000
            # if y != 32767:
            #     y = 2000 - (y * 8)

            print('x: ' + str(x) + ' y: ' + str(y))
            robot.drive(x, y) # drive(self, velocity, radius)
