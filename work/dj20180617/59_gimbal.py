from dronekit import connect,VehicleMode
import time

vehicle = connect("127.0.0.1:14550", wait_ready=True)

vehicle.mode = VehicleMode("GUIDED")
vehicle.armed = True
while not vehicle.mode.name == "GUIDED" and not vehicle.armed == True and not api.exit:
    print("waiting arm")
    time.sleep(1)

vehicle.gimbal.rotate(-90, 0, 0)
time.sleep(10)

vehicle.gimbal.target_location(vehicle.home_location)
time.sleep(10)