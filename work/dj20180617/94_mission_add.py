from dronekit import connect,Command,mavutil

vehicle = connect('127.0.0.1:14550', wait_ready=True)

cmds = vehicle.commands

cmds.download()
cmds.wait_ready()

cmd = Command(
    0, 0, 0,
    mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
    mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
    0,0,0,0,0,0,0,0,
    10
)
cmds.add(cmd)

cmds.upload()
