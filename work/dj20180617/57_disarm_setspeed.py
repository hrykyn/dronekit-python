from dronekit import connect
import time

vehicle = connect('127.0.0.1:14550', wait_ready=True)

vehicle.armed = False
    
vehicle.groundspeed = 3.2