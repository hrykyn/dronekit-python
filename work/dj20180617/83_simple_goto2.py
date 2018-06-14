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

def degToRad(deg):
    return deg * math.pi/180

def radToDeg(rad):
    return rad * 180/math.pi


# http://python.dronekit.io/guide/copter/guided_mode.html#guided-mode-copter-useful-conversion-functions
def getLocationMetres(originalLocation, dNorth, dEast, dAlt):
    earthRadius = 6378137.0 #Radius of "spherical" earth
    # Coordinate offsets in radians
    dLat = dNorth/earthRadius
    dLon = dEast/(earthRadius*math.cos(degToRad(originalLocation.lat)))

    # New position in decimal degrees
    newLat = originalLocation.lat + radToDeg(dLat)
    newLon = originalLocation.lon + radToDeg(dLon)
    if dAlt:
        newAlt = originalLocation.alt + dAlt

    if type(originalLocation) is dk.LocationGlobal:
        targetLocation = dk.LocationGlobal(newLat, newLon, newAlt)
    elif type(originalLocation) is dk.LocationGlobalRelative:
        targetLocation = dk.LocationGlobalRelative(newLat, newLon, newAlt)
    else:
        raise Exception("Invalid Location object passed")

    return targetLocation
    

arm_and_takeoff(20)
currentLocation = vehicle.location.global_relative_frame
targetLocation = getLocationMetres(currentLocation, 10, 10, 5)
print targetLocation

#vehicle.simple_goto(targetLocation)
vehicle.simple_goto(targetLocation, groundspeed=2)

