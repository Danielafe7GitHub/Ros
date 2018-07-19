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
from cv_bridge import CvBridge, CvBridgeError

d1 = 0
d2 = 0
def callback(data):
    global d1
    global d2
    print("X: ",data.x," Y: ",data.y)
    d1 = int(data.x)
    d2 = int(data.y) 

def talker(data):
    image = None
    bridge = CvBridge()
    try:
        image = bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
        print(e)
    output = image.copy()   

    # Centro QR Code (d1,d2)
    cv2.circle(output,(d1,d2), 5, (0,0,255), -1)    

    # Centro Video Frame (c1,c2)
    c1 = 320
    c2 = 180
    cv2.circle(output,(c1,c2), 20, (0,90,255), -1)
    cv2.line(output,(c1,c2),(d1,d2),(0,0,255),5)

    #print("Centro Frame :",c1, " ",c2)
    #print("Centro QR code :",d1, " ",d2)
    # Movimientos
    if c1 < d1:
        print("Muevete a la derecha !!!")
    if c1 > d1:
        print("Muevete a la izquierda !!!")
    if c2 > d2:
        print("Muevete hacia arriba !!!")
    if c2 < d2:
        print("Muevete hacia abajo !!!")


    cv2.imshow("Image", output)
    cv2.waitKey(3)

def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("preprocesamiento", vector21, callback)
    rospy.Subscriber("/ardrone/front/image_raw", Image, talker)

    rospy.spin()

if __name__ == '__main__':
    listener()
