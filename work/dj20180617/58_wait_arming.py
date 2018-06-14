from dronekit import connect,VehicleMode
import time

vehicle = connect('127.0.0.1:14550', wait_ready=True)

vehicle.mode = VehicleMode("GUIDED")

# arming
vehicle.armed = True

# wait until mode becomes GUIDED mode and arming
while not vehicle.mode.name == 'GUIDED' and not vehicle.armed and not api.exit:
    time.sleep(1)

print "armed"