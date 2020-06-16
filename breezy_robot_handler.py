import logging
import math
from breezycreate2 import Robot


#logging.basicConfig(level=logging.DEBUG)

# Max radius we want to use. 2000 may turn to slowly
MAX_RADIUS = 1200

def clamp(value, smallest, largest): 
    return max(smallest, min(value, largest))

class RobotHandler:
    def init_bot(self):
        global robot
        #robot = Robot()
        #robot = Robot("65000", "57600")
        robot = Robot('sim')
        logging.debug('robot created at port')


    def stop(self):
        go({'X': 0, 'Y': 0})


    def turn(self, data):
        velocity = data['Velocity']
        direction = math.copysign(1, -velocity) 
        velocity = math.fabs(velocity)

        
        print('velocity: ' + str(velocity) + ' direction: ' + str(direction))

        robot.drive(velocity, direction)
        
    def go(self, data):
        x = data['X']
        y = data['Y']
     
        velocity = math.sqrt(x * x + y * y)  
        velocity = math.copysign(velocity * 2.5, -y) #scale and fix direction
        radius = 0
        if x != 0: #sign of x determines turn direction
            radius = (math.sin(math.atan(math.fabs(y)/x)) * MAX_RADIUS) + 1
 

        # radius: A number between -2000 and 2000. Units are mm.  
        radius = clamp(radius, -2000, 2000)
        # velocity: A number between -500 and 500. Units are mm/s. 
        velocity = clamp(velocity, -500, 500)
        
        # Increase area of "stop"
        if math.fabs(velocity) < 30:
            velocity = 0

        # If radius is very small, drive straight
        if math.fabs(radius) > MAX_RADIUS - 20:
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


    def go_direct(self, data):
        x = data['X']
        y = data['Y']

        y = -y #ui bug, fix there

        velocity = math.sqrt(x * x + y * y)  
        velocity = math.copysign(velocity * 2.5, y) #scale and fix direction

        if x == 0:
            angle = 0
        else:
            angle = math.atan(y/x)

        if angle == math.fabs(angle):
            r = velocity * math.sin(math.fabs(angle))
            l = velocity
        else:
            r = velocity
            l = velocity * math.sin(math.fabs(angle))
 
        
        
        

        print('x: ' + str(x) + 'y: ' + str(y) )
        print('v: ' + str(velocity) + 'a: ' + str(angle) + ' r: ' + str(r) + ' l: ' + str(l))
        robot.drive_direct(r, l) 
