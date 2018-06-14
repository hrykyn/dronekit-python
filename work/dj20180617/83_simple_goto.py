import dronekit as dk
import time
import math

vehicle = dk.connect('127.0.0.1:14550', wait_ready=True)

def arm_and_takeoff(targetAltitude):
    print("Basic pre-arm checks")
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    vehicle.mode = dk.VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.mode.name == 'GUIEDED' and not vehicle.armed:
        print 'waiting for arming...'
        time.sleep(1)

    vehicle.simple_takeoff(targetAltitude)
    while True: 
        currentAltitude = vehicle.location.global_relative_frame.alt
        print "Altitude: ", currentAltitude

        if currentAltitude >= targetAltitude * 0.95:
            print "Reached target altitude (%s)" % targetAltitude
            break

        time.sleep(1)

    print "lastAltitude: ", vehicle.location.global_relative_frame.alt

arm_and_takeoff(20)
targetLocation = dk.LocationGlobalRelative(-34.364114, 149.166022, 20)

#vehicle.simple_goto(targetLocation)
vehicle.simple_goto(targetLocation, groundspeed=2)

