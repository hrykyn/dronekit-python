#!/usr/bin/env python

import time

from dronekit import connect, VehicleMode, LocationGlobalRelative, Command, LocationGlobal
from pymavlink import mavutil

def arm_and_takeoff(altitude):
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

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(altitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto
    #  (otherwise the command after Vehicle.simple_takeoff will execute
    #   immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= altitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)
	

def clear_mission(vehicle):
	# clear missions and download mission again
	cmds = vehicle.commands
	cmds.clear()
	vehicle.flush()

	download_mission(vehicle)

def download_mission(vehicle):
	cmds = vehicle.commands
	cmds.download()
	cmds.wait_ready()

def get_current_mission(vehicle):
	# get current mission and return missionList and number of waypoints
	cmds = vehicle.commands
	download_mission(vehicle)
	missionList = []
	n_wp        = 0

	for wp in cmds:
		print wp
		missionList.append(wp)
		n_wp +=1

	return n_wp, missionList

def add_last_waypoint_to_mission(vehicle, lat, long, alt):
	download_mission(vehicle)
	cmds = vehicle.commands

	missionList = []
	for wp in cmds:
		missionList.append(wp)

	# add last waypoint(here is an example of adding waypoint)
	wp_last = Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
				0, 0, 0, 0, 0, 0,
				lat, long, alt);
	missionList.append(wp_last)

	cmds.clear()

	for wp in missionList:
		cmds.add(wp)

	cmds.upload()

	return (cmds.count)


def ChangeMode(vehicle, mode):
	# change mode to given mode
	while vehicle.mode != VehicleMode(mode):
		vehicle.mode = VehicleMode(mode);
		time.sleep(0.5)
	
	return True;
	

def main(vehicle):
	gnd_speed = 10
	mode = 'GROUND'
	pre_mode = ''
	
	while True:
		if pre_mode != mode:
			print("Mode Switched from [%s] to [%s]" %(pre_mode, mode))

		if mode == 'GROUND':
			n_wp, missionList = get_current_mission(vehicle)
			time.sleep(2)
	
			if n_wp > 0:
				print('A valid mission has been uploaded: takeoff!')
				mode = 'TAKEOFF'
		
		elif mode == 'TAKEOFF':
			# add "launch point" to last waypoint
			add_last_waypoint_to_mission(vehicle,
							vehicle.location.global_relative_frame.lat,
							vehicle.location.global_relative_frame.lon,
							vehicle.location.global_relative_frame.alt
							)
	
			print("Final waypoint added to the current mission")
			time.sleep(1)
	
			# take off to 10m altitude
			arm_and_takeoff(10)
	
			# enter auto mode to start mission
			ChangeMode(vehicle, "AUTO")
	
			vehicle.groundspeed = gnd_speed
	
			mode = 'MISSION'
	
		elif mode == 'MISSION':
			print("CurrentWP: %d of %d " %(vehicle.commands.next, vehicle.commands.count))
	
			if(vehicle.commands.next == vehicle.commands.count):
				print ("Final wp reached: go back home")
				
				clear_mission(vehicle)
				print ("Mission deleted")
					
				ChangeMode(vehicle, "RTL")
	
				mode = 'BACK'

		elif mode == 'BACK':
			if vehicle.location.global_relative_frame.alt < 1.0:
				print("Vehicle landed, back to GROUND")
				mode = 'GROUND'
		
		pre_mode = mode
		time.sleep(0.5)


vehicle = connect('udp:127.0.0.1:14550', wait_ready=True)
main(vehicle)
