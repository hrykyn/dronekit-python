from dronekit import connect,Command,mavutil

vehicle = connect('127.0.0.1:14550', wait_ready=True)

cmds = vehicle.commands

cmds.download()
cmds.wait_ready()

missionList = []
for cmd in cmds:
    missionList.append(cmd)

missionList[0].command = mavutil.mavlink.MAV_CMD_NAV_TAKEOFF

cmds.clear()

for cmd in missionList:
    cmds.add(cmd)
    cmds.upload()