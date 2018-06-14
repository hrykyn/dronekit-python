from dronekit import connect
import time

vehicle = connect('127.0.0.1:14550', wait_ready=True)
vehicle.parameters['THR_MIN'] = 120

@vehicle.parameters.on_attribute('THR_MIN')
def decorated_thr_min_callback(self, attr_name, value):
    print "PARAMETER CALLBACK %s changed to %s" % (attr_name, value)

print vehicle.parameters['THR_MIN']
time.sleep(1)

vehicle.parameters['THR_MIN'] = 110