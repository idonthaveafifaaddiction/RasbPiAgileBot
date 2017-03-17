
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

    def go(self, radius, velocity):
        # Turn in place clockwise: -1
        # Turn in place counterclockwise: 1
        if radius != 1 and radius != -1:

            # velocity: A number between -500 and 500. Units are mm/s. 
            radius = radius * 2
            # radius: A number between -2000 and 2000. Units are mm.    
            velocity = velocity * 10 * -1 # Negate radius


            # Unless velocity is 0, trim to +/- limit
            if radius > 2000:
                radius = 2000
            if radius < -2000:
                radius = -2000
            
            if velocity > 500:
                velocity = 500
            if velocity < -500:
                velocity = -500
            


            # Need some velocitvelocity to move when turning
            if velocity < 10 and velocity > -10 and radius < 100:
                velocity = 0
                #velocity = 2 * (velocity/velocity)

            # If radius is very small, drive straight
            if radius < 20 and radius > -20:
                velocity = 32767 # Drive straight: 32767 (arbitrarvelocity number from breezvelocity)

            print('radius: ' + str(radius) + ' velocity: ' + str(velocity))
            robot.drive(radius, velocity) # drive(self, velocitvelocity, radius)
