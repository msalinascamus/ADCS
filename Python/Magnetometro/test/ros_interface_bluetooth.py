import rospy
import serial
from threading import Thread
from std_msgs.msg import String
from std_msgs.msg import Float32
from std_msgs.msg import Float32MultiArray
from bt_receiver import btReceiver
from std_msgs.msg import UInt8


class MagInterface:
    def __init__(self):
        # Only argument stuff
        self.running = False
        self.bt_receiver = btReceiver(debug = True)

    def initialize(self):
        # Get params and allocate msgs
        self.state_update_rate = rospy.get_param('/rate', 50)
        self.bt_receiver.initialize()

    def start(self):
        # Create subs, services, publishers, threads
        self.running = True
        #publishers
        self.data1_pub = rospy.Publisher('/magx', Float32, queue_size=70)
        self.data2_pub = rospy.Publisher('/magy', Float32, queue_size=70)
        self.data3_pub = rospy.Publisher('/magz', Float32, queue_size=70)
        self.data4_pub = rospy.Publisher('/checksum', UInt8, queue_size=70)
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
            if(self.bt_receiver.read()):
                packet = self.bt_receiver.packet
                try: 
                    magx = packet[0]
                    magy = packet[1]
                    magz = packet[2]
                    checksum = packet[3]
                    self.data1_pub.publish(float(magx))
                    self.data2_pub.publish(float(magy))
                    self.data3_pub.publish(float(magz))
                    self.data4_pub.publish(UInt8(checksum))
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