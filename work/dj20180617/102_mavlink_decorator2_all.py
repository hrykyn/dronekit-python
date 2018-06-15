from dronekit import connect,VehicleMode
import time

vehicle = connect('127.0.0.1:14550', wait_ready=True)

@vehicle.on_message('*')
def listener(self, name, message):
    print "%s: %s" % (name, message)


while not vehicle.is_armable:
    print "Waiting for vehicle to initialize..."
    time.sleep(1)


print "Arming motors"
vehicle.mode = VehicleMode("GUIDED")
vehicle.armed = True

while not vehicle.armed and not vehicle.mode.name == 'GUIDED':
    print "Waiting for arming..."
    time.sleep(1)


targetAltitude = 20

print "Take off!!!"
vehicle.simple_takeoff(targetAltitude)

while True:
    currentAltitude = vehicle.location.global_relative_frame.alt
    print "Altitude: ", currentAltitude

    if currentAltitude >= targetAltitude * 0.95:
        print "Reached target altitude (%s)" % targetAltitude
        break
    
    time.sleep(1)
