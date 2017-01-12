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
        if x > -500 and x < 500 and y > -500 and y < 500:
            print('x: ' + str(x) + ' y: ' + str(y))
            robot.drive(y * 2, x / 2)


