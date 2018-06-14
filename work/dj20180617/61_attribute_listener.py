from dronekit import connect
import time

print "[%s]" % (time.strftime("%Y/%m/%d %H:%M:%S"))
def location_callback(self, attr_name, value):
    print "[%s] %s: %s" % (time.strftime("%Y/%m/%d %H:%M:%S"), attr_name, value)

vehicle = connect("127.0.0.1:14550", wait_ready=True)


vehicle.add_attribute_listener('location.global_frame', location_callback)

time.sleep(10)


vehicle.remove_attribute_listener('location.global_frame', location_callback)