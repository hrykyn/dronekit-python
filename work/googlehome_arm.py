#!/usr/bin/env python
# control from google home
#
import time

from dronekit import connect, VehicleMode
from pymavlink import mavutil

import websocket
import thread

def arm():
    """
    Arms vehicle and fly to a target altitude.
    """

    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)


def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    arm()

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto
    #  (otherwise the command after Vehicle.simple_takeoff will execute
    #   immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)

def ChangeMode(vehicle, mode):
	# change mode to given mode
	while vehicle.mode != VehicleMode(mode):
		vehicle.mode = VehicleMode(mode);
		time.sleep(0.5)
	
	return True;
	


##################
# web socket client
##################
def on_message(ws, message):
    print message
    if(message == 'arm_and_takeoff'):
        arm_and_takeoff(10);
	time.sleep(3)
	ChangeMode(vehicle, "RTL")

def on_error(ws, error):
    print error

def on_close(ws):
    print "### closed ###"


vehicle = connect('udp:127.0.0.1:14550', wait_ready=True)

websocket.enableTrace(True)
ws = websocket.WebSocketApp("ws://184.72.178.158:3000/ws",
                          on_message = on_message,
                          on_error = on_error,
                          on_close = on_close)
ws.run_forever()


