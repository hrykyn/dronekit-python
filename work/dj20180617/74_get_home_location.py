from dronekit import connect
import time

vehicle = connect('127.0.0.1:14550', wait_ready=True)

wait_num = 0

# need to download commands(mission) to get HomeLocation
while not vehicle.home_location:
    cmds = vehicle.commands 
    cmds.download()
    cmds.wait_ready()

    if not vehicle.home_location:
        print "Waiting for home location... (%s)" % wait_num
        wait_num += 1
    
    time.sleep(0.1)
    
print "\n Home location: %s\n\n" % vehicle.home_location