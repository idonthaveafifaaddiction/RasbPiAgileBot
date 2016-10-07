import serial
import logging

logging.basicConfig(level=logging.DEBUG)
port = '/dev/ttyUSB0'

class RobotHandler:
    def init_bot(self, port):
	try:
            connection = serial.Serial(port, baudrate=115200, timeout=1)
            print "Connected!"
        except:
            print "Failed."
        global robot
        robot = create.Create(port)
        logging.debug('robot created at port: ' + port)

    def go(self, x, y):
        if x > -250 and x < 250 and y > -250 and y < 250:
            robot.go(x,y)

