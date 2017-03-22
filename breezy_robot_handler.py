
from breezycreate2 import Robot
import logging
import time
from math import sqrt  

logging.basicConfig(level=logging.DEBUG)

# Serial port constants
COMPORT_SIM = 'sim'

def clamp(n, smallest, largest): return max(smallest, min(n, largest))

class RobotHandler:
    def init_bot(self, port):
        global robot
        robot = Robot()
        #robot = create.Create(port)
        logging.debug('robot created at port')


    def go(self, x, y):
        velocity = sqrt(x * x + y * y)  
        radius = x

        # Turn in place clockwise: -1
        # Turn in place counterclockwise: 1
        if radius != 100000 and radius != -1000000:

            # velocity: A number between -500 and 500. Units are mm/s. 
            velocity = velocity * 2 * (y/y) # Negate radius
            # radius: A number between -2000 and 2000. Units are mm.    
            radius = radius * 10 * -1


            # Trim to +/- limit
            radius = clamp(radius, -2000,2000)
            velocity = clamp(velocity, -500, 500)
            
            # Need some velocity to move when turning
            if velocity < 10 and velocity > -10:
                velocity = 0
                #velocity = 2 * (velocity/velocity)

            # If radius is very small, drive straight
            if radius < 20 and radius > -20:
                radius = 32767 # Drive straight: 32767 (arbitrary number from breezy)

            #-1 is fast left turn, -2000 is slow left
            elif radius < 0:
                radius = -2002 - radius
            elif radius > 0:
                radius = 2002 - radius

            print('radius: ' + str(radius) + ' velocity: ' + str(velocity))
            robot.drive(velocity, radius) # drive(self, velocity, radius)
