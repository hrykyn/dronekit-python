from dronekit import connect,VehicleMode,Command,mavutil,LocationGlobal,LocationGlobalRelative
import time
import math

vehicle = connect('127.0.0.1:14550', wait_ready=True)

vehicle.mode = VehicleMode("GUIDED")
while not vehicle.mode.name == "GUIDED":
    time.sleep(1)

vehicle.mode = VehicleMode("AUTO")

cmds = vehicle.commands
cmds.download()
cmds.wait_ready()

vehicle.mode = VehicleMode("AUTO")

def distance_to_last_waypoint():
    missionitem=cmds[cmds.count-1] #commands are zero indexed
    lat=missionitem.x
    lon=missionitem.y
    alt=missionitem.z
    targetWaypointLocation=LocationGlobalRelative(lat,lon,alt)
    distancetopoint = get_distance_metres(vehicle.location.global_frame, targetWaypointLocation)
    print distancetopoint
    return distancetopoint

def get_distance_metres(aLocation1, aLocation2):
    """
    Returns the ground distance in metres between two `LocationGlobal` or `LocationGlobalRelative` objects.

    This method is an approximation, and will not be accurate over large distances and close to the
    earth's poles. It comes from the ArduPilot test code:
    https://github.com/diydrones/ardupilot/blob/master/Tools/autotest/common.py
    """
    dlat = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon
    distance = math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5
    return distance

while distance_to_last_waypoint() > 1:
    time.sleep(1)