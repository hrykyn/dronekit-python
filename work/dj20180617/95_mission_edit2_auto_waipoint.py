from dronekit import connect,Command,mavutil,LocationGlobal,LocationGlobalRelative
import math

vehicle = connect('127.0.0.1:14550', wait_ready=True)

def degToRad(deg):
    return deg * math.pi/180

def radToDeg(rad):
    return rad * 180/math.pi

# http://python.dronekit.io/guide/copter/guided_mode.html#guided-mode-copter-useful-conversion-functions
def getLocationMetres(originalLocation, dNorth, dEast, dAlt=0):
    earthRadius = 6378137.0 #Radius of "spherical" earth
    # Coordinate offsets in radians
    dLat = dNorth/earthRadius
    dLon = dEast/(earthRadius*math.cos(degToRad(originalLocation.lat)))

    # New position in decimal degrees
    newLat = originalLocation.lat + radToDeg(dLat)
    newLon = originalLocation.lon + radToDeg(dLon)
    newAlt = originalLocation.alt + dAlt

    if type(originalLocation) is LocationGlobal:
        targetLocation = LocationGlobal(newLat, newLon, newAlt)
    elif type(originalLocation) is LocationGlobalRelative:
        targetLocation = LocationGlobalRelative(newLat, newLon, newAlt)
    else:
        raise Exception("Invalid Location object passed")

    return targetLocation

cmds = vehicle.commands
cmds.download()
cmds.wait_ready()

cmds.clear()

cmd = Command(
    0, 0, 0,
    mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
    mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
    0,0,0,0,0,0,0,0,
    10
)
cmds.add(cmd)
    
currentLocation = vehicle.location.global_relative_frame

targetLocation = getLocationMetres(currentLocation, 10, 10, 5)
cmd = Command( 0, 0, 0,
    mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
    mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
    0,0,
    0,0,0,0,
    targetLocation.lat,targetLocation.lon,targetLocation.alt
)
cmds.add(cmd)

targetLocation = getLocationMetres(targetLocation, 10, -10)
cmd = Command( 0, 0, 0,
    mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
    mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
    0,0,0,0,0,0,
    targetLocation.lat,targetLocation.lon,targetLocation.alt
)
cmds.add(cmd)


cmds.upload()
