import create
import time
from breezycreate2 import Robot

robot = create.Create('sim')
#robot = Robot("65000", "57600")

def write_sensors():
    # robot.robot.get_packet(19)
    # robot.robot.get_packet(20)
    # print('distance: ', robot.robot.sensor_state['distance'])
    # print('angle: ', robot.robot.sensor_state['angle'])
    print('RIGHT_VELOCITY: ', robot.getSensor('RIGHT_VELOCITY'))
    print('LEFT_VELOCITY: ', robot.getSensor('LEFT_VELOCITY'))
 
write_sensors()
robot.drive(100, 1500)
time.sleep(1)

write_sensors()
time.sleep(1)

write_sensors()
time.sleep(1)

write_sensors()

robot.drive(-200, 500)
time.sleep(1)

# write_sensors()
time.sleep(1)

write_sensors()
robot.shutdown()
