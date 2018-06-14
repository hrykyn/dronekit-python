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


velocity_x = 3 # NorthSouth(m/s)
velocity_y = 6 # EastWest(m/s)
velocity_z = 1 # DownUp(m/s)
duration = 5

msg = vehicle.message_factory.set_position_target_local_ned_encode(
    0,
    0,0,
    dk.mavutil.mavlink.MAV_FRAME_LOCAL_NED,
    0b0000111111000111,
    0,0,0,
    velocity_x, velocity_y, velocity_z,
    0,0,0,
    0,0
)

for x in range(0, duration):
    vehicle.send_mavlink(msg)
    time.sleep(1)