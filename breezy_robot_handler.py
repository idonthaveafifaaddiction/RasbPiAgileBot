import logging
import math
from breezycreate2 import Robot


logging.basicConfig(level=logging.DEBUG)

def clamp(value, smallest, largest): 
    return max(smallest, min(value, largest))

class RobotHandler:
    def init_bot(self):
        global robot
        #robot = Robot("65000", "57600")
        robot = Robot('sim')
        logging.debug('robot created at port')


    def go(self, data):
        x = data['X']
        y = data['Y']
     
        velocity = math.sqrt(x * x + y * y)  
        velocity = math.copysign(velocity * 2, -y) #scale and fix direction
        radius = 0
        if x != 0: #sign of x determines turn direction
            radius = (math.sin(math.atan(math.fabs(y)/x)) * 1200) + 1
 

        # radius: A number between -2000 and 2000. Units are mm.  
        radius = clamp(radius, -2000, 2000)
        # velocity: A number between -500 and 500. Units are mm/s. 
        velocity = clamp(velocity, -500, 500)
        
        # Increase area of "stop"
        if math.fabs(velocity) < 30:
            velocity = 0

        # If radius is very small, drive straight
        if math.fabs(radius) > 1190:
            radius = 32767
        elif math.fabs(radius) < 10:
            radius = math.copysign(1, -radius)
        
        #only allow backup to be straight
        if velocity <= 0:
            radius = 32767

        # Convert to ints before sending
        velocity = math.floor(velocity)
        radius = math.floor(radius)

        print('velocity: ' + str(velocity) + ' radius: ' + str(radius))
        robot.drive(velocity, radius) # drive(self, velocity, radius)
