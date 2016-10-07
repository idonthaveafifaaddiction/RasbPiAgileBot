import create
import time
robot = create.Create('/dev/ttyUSB0')
robot.go(0, 100)
time.sleep(10)
robot.stop()
#robot.seekDock()
