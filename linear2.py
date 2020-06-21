from gpiozero import Motor

import time

motor = Motor("BOARD37", "BOARD35", "BOARD7")
motor.forward()


time.sleep(3)

motor.stop()
