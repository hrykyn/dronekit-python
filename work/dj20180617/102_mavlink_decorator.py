from dronekit import connect
import time

vehicle = connect('127.0.0.1:14550', wait_ready=True)

@vehicle.on_message('RANGEFINDER')
def listener(self, name, message):
    print "distance: %s" % message.distance
    print "voltage: %s" % message.voltage
