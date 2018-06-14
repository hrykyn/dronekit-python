from dronekit import connect,VehicleMode,Command,mavutil
import time

vehicle = connect('127.0.0.1:14550', wait_ready=True)

vehicle.mode = VehicleMode("GUIDED")
while not vehicle.mode.name == "GUIDED":
    time.sleep(1)

vehicle.mode = VehicleMode("AUTO")

cmds = vehicle.commands
cmds.download()
cmds.wait_ready()

missionList = []
for cmd in cmds:
    missionList.append(cmd)

missionList.append(missionList[-1])
cmds.clear()

for cmd in missionList:
    cmds.add(cmd)

cmds.upload()

vehicle.mode = VehicleMode("AUTO")


while not cmds.count == cmds.next:
    print 
    time.sleep(1)