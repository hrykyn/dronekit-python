from dronekit import connect
import time

vehicle = connect('127.0.0.1:14550', wait_ready=True)

print "Param: %s" % vehicle.parameters["THR_MIN"]

time.sleep(3)

vehicle.parameters["THR_MIN"] = 100

time.sleep(3)

print "Param: %s" % vehicle.parameters["THR_MIN"]