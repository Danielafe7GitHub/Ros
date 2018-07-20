#!/usr/bin/env python
import rospy
from ardrone_autonomy.msg import vector21
import sys
import operator
import cv2
import zbar
import numpy as np
from std_msgs.msg import String
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge, CvBridgeError

#Variables Globales
d1 = None
d2 = None
texto = ""
texto2 = ""
t_x = 0
t_y = 0
vel_lin = 0.4
vel_ang = 0.5
mov = Twist() 

def callback(data):
    global d1
    global d2
    #print("X: ",data.x," Y: ",data.y)
    d1 = int(data.x)
    d2 = int(data.y) 
    if d1 == 0 and d2 == 0:
        d1 = None
        d2 = None

def talker(data,param):
    global texto
    global texto2
    global t_x
    global t_y
    image = None
    bridge = CvBridge()
    try:
        image = bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
        print(e)

    # Centro Video Frame (c1,c2)
    height, width, channels = image.shape
    c1 = width / 2
    c2 = height / 2
    cv2.circle(image,(c1,c2), 20, (0,90,255), -1)
    

    if d1 != None and d2 != None:
        # Centro QR Code (d1,d2)
        cv2.circle(image,(d1,d2), 5, (0,0,255), -1) 
        cv2.line(image,(c1,c2),(d1,d2),(0,0,255),5)   
        # Movimientos
        if c1 < d1:
            mov.linear.x = vel_lin  * (-1)
            t_x = 500
            texto = "Derecha"
            #print("Muevete a la derecha !!!")
        #if c1 > d1:
        else:
            mov.linear.x = vel_lin * (1)
            t_x = 0
            texto = "Izquierda"
            #print("Muevete a la izquierda !!!")

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(image,texto,(t_x,180), font, 1,(255,255,255),2)
        param.publish(mov)
        if c2 > d2:
            mov.linear.y = vel_lin  * (-1)
            t_y = 30
            texto2 = "Arriba"
            #print("Muevete hacia arriba !!!")
        #if c2 < d2:
        else:
            mov.linear.y = vel_lin * (1)
            t_y = 320
            texto2 = "Abajo"
            #print("Muevete hacia abajo !!!")

        param.publish(mov)
        mov.linear.x = 0 
        mov.linear.y = 0 
        mov.linear.z = 0 
        param.publish(mov)
        
        cv2.putText(image,texto2,(320,t_y), font, 1,(255,255,255),2)


    
    
    cv2.imshow("Image", image)
    cv2.waitKey(3)

def listener():
    rospy.init_node('listener', anonymous=True)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 1)
    rospy.Subscriber("preprocesamiento", vector21, callback)
    rospy.Subscriber("/ardrone/front/image_raw", Image, talker, pub)

    rospy.spin()

if __name__ == '__main__':
    listener()
