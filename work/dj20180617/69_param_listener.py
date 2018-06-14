from dronekit import connect
import time

vehicle = connect("127.0.0.1:14550", wait_ready=True)
vehicle.parameters['THR_MIN'] = 120

def thr_min_parameter_callback(self, attr_name, value):
    print "%s: %s" % (attr_name, value)

vehicle.parameters.add_attribute_listener('THR_MIN', thr_min_parameter_callback)

print vehicle.parameters['THR_MIN']
time.sleep(1)

vehicle.parameters['THR_MIN'] = 110