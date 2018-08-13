#!/usr/bin/python

__author__ = 'gdiaz'

# ROS INTERFACE

"""Provides a high level interface over ROS for bluetooth data exchange.
"""

import rospy
import serial
from threading import Thread
from std_msgs.msg import String
from std_msgs.msg import Float32
from std_msgs.msg import Float32MultiArray

class MagInterface:
    def __init__(self):
        # Only argument stuff
        self.running = False

    def initialize(self):
        # Get params and allocate msgs
        self.state_update_rate = rospy.get_param('/rate', 50)
        self.serial = serial.Serial('/dev/ttyACM0', 115200, timeout=2) 
        
    def start(self):
        # Create subs, services, publishers, threads
        self.running = True
        #publishers
        self.data1_pub = rospy.Publisher('/magx', Float32, queue_size=70)
        self.data2_pub = rospy.Publisher('/magy', Float32, queue_size=70)
        self.data3_pub = rospy.Publisher('/magz', Float32, queue_size=70)
        self.data4_pub = rospy.Publisher('/d', Float32, queue_size=70)
        Thread(target=self.update_state).start()

    def stop(self):
        self.running = False

        self.data1_pub.unregister()
        self.data2_pub.unregister()
        self.data3_pub.unregister()
        self.data4_pub.unregister()

    def update_state(self):
        rate = rospy.Rate(self.state_update_rate)
        while self.running and not rospy.is_shutdown():
		data = self.serial.readline()
		try: 
		  magx, magy, magz, d = data.split(';')
		  print (magx, magy, magz, d)
                  self.data1_pub.publish(float(magx))
	          self.data2_pub.publish(float(magy))
	          self.data3_pub.publish(float(magz))
                  self.data4_pub.publish(float(d))
	        except: 
		  print ("incomplete data")
                rate.sleep()
						   
	       

if __name__ == '__main__':
    rospy.init_node('ros_bt_interface')
    mg_ros = MagInterface()
    mg_ros.initialize()
    mg_ros.start()
    rospy.spin()
    mg_ros.stop()
