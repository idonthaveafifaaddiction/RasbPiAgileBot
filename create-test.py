import create
import time
robot = create.Create('sim')
robot.go(0, 100)
time.sleep(20)
robot.stop()
#robot.seekDock()
