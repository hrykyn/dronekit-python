from dronekit import connect,VehicleMode

vehicle = connect('127.0.0.1:14550', wait_ready=True)

vehicle.mode = VehicleMode("AUTO")