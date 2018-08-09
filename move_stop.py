#! /usr/bin/env python

import rospy 
from geometry_msgs.msg import Twist
import time



rospy.init_node('twist_publisher') #Crea el publicador
pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 1) #Le dice hey publicare en counter que ya se tipo msh es Int32
rate = rospy.Rate(5)
mov = Twist() #Creo variable de ese tipo
mov.linear.y = 0 #Accedo al atributo del msg
speed = 0.5
distance = 1


while not rospy.is_shutdown():

        #Setting the current time for distance calculus
        t0 = rospy.Time.now().to_sec()
        current_distance = 0

        #Loop to move the turtle in an specified distance
        while current_distance < distance:
            #Publish the velocity
            pub.publish(mov) 
            mov.linear.y = speed
            pub.publish(mov) 
            #Takes actual time to velocity calculus
            t1=rospy.Time.now().to_sec()
            #Calculates distancePoseStamped
            current_distance= speed*(t1-t0)
            print("Current: ",current_distance)
            
        #After the loop, stops the robot
        print("Out...........................................................................")
        mov.linear.y = 0
        #Force the robot to stop
        pub.publish(mov) 
        time.sleep(1)
        #rate.sleep()


'''while not rospy.is_shutdown():
    pub.publish(mov) 
    rate.sleep()'''

