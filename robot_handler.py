import create
import logging

logging.basicConfig(level=logging.DEBUG)

# Serial port constants
COMPORT_SIM = 'sim'

class RobotHandler:
    def init_bot(self, port):
        global robot
        robot = create.Create(port)
        logging.debug('robot created at port: ' + port)

    def go(self, x, y):
        if x > -250 and x < 250 and y > -250 and y < 250:
            robot.go(x,y)
