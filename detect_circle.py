#!/usr/bin/env python
import sys
import rospy
import cv2
import numpy as np
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

def callback_image(data):
    image = None
    bridge = CvBridge()
    try:
        image = bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
        print(e)
    output = image.copy()
   

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img = cv2.medianBlur(gray, 3)
    img = cv2.GaussianBlur(img,(9,9),2,2)
    circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,
                            param1=50,param2=30,minRadius=0,maxRadius=0)

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            cv2.circle(img, (x, y), r, (0, 255, 0), 4)
    cv2.imshow("Image", img)
    cv2.waitKey(3)


if __name__ == '__main__':
    rospy.init_node('Track')
    rospy.Subscriber("/drone/front_camera/image_raw", Image, callback_image)
    rospy.spin()
   
    cv2.destroyAllWindows()
