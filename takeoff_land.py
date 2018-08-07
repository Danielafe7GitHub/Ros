#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty

vel_linear = 0.3
vel_angular = 0.6

landed = False

def keys_cb(msg):
	global landed
	if len(msg.data) != 0:
		if msg.data[0] == 's':
			landed = not landed
		return # unknown key

if __name__ == '__main__':
	rospy.init_node('keys_to_twist')
	takeoff_pub = rospy.Publisher("ardrone/takeoff", Empty, queue_size=10 )
	land_pub = rospy.Publisher("ardrone/land", Empty, queue_size=10 )
	rospy.Subscriber('keys', String, keys_cb)
	rate = rospy.Rate(30)
	while not rospy.is_shutdown():
		if landed:
			takeoff_pub.publish(Empty())
		else:
			land_pub.publish(Empty())
		rate.sleep()
