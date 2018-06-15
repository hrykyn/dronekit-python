from dronekit import connect
import time

vehicle = connect('127.0.0.1:14550', wait_ready=True)

def listener(self, name, message):
    print "distance: %s" % message.distance
    print "voltage: %s" % message.voltage

vehicle.add_message_listener('RANGEFINDER', listener)

time.sleep(10)


vehicle.remove_message_listener('RANGEFINDER', listener)
