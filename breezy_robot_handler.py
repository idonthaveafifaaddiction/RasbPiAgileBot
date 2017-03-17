
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
        if radius != 100000 and radius != -1000000:

            # velocity: A number between -500 and 500. Units are mm/s. 
            velocity = velocity * 2 * -1 # Negate radius
            # radius: A number between -2000 and 2000. Units are mm.    
            radius = radius * 7 * -1


            # Unless velocity is 0, trim to +/- limit
            if radius > 1990:
                radius = 1990
            if radius < -1990:
                radius = -1990
            
            if velocity > 450:
                velocity = 450
            if velocity < -450:
                velocity = -450
            


            # Need some velocitvelocity to move when turning
            if velocity < 10 and velocity > -10 and radius < 100:
                velocity = 0
                #velocity = 2 * (velocity/velocity)

            # If radius is very small, drive straight
            if radius < 20 and radius > -20:
                radius = 32767 # Drive straight: 32767 (arbitrarvelocity number from breezvelocity)

            print('radius: ' + str(radius) + ' velocity: ' + str(velocity))
            robot.drive(velocity, radius) # drive(self, velocitvelocity, radius)
