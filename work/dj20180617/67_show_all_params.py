from dronekit import connect
import time

vehicle = connect('127.0.0.1:14550', wait_ready=True)

for key,value in vehicle.parameters.iteritems():
    print "Key: %s Value: %s" % (key, value)