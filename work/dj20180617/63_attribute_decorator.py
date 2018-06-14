from dronekit import connect
import time

vehicle = connect('127.0.0.1:14550', wait_ready=True)

#last_rangefinder_distance = 0
#@vehicle.on_attribute('rangefinder')
#def range_finder_callback(self, attr_name):
#    global last_rangefinder_distance
#
#    if(last_rangefinder_distance == round(self.rangefinder.distance, 1)):
#        return
#    
#    last_rangefinder_distance = round(self.rangefinder.distance, 1)
#    print "RangeFinder(meters): %s" % (last_rangefinder_distance)

@vehicle.on_attribute('location.global_frame')
def listener(self, name, msg):
    print '%s : %s' % (name, msg)

time.sleep(10)