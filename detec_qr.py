#!/usr/bin/env python
import sys
import rospy
import operator
import cv2
import zbar
from PIL import Image
import numpy as np
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from array import array

def callback_image(data):
    image = None
    bridge = CvBridge()
    try:
        image = bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
        print(e)
    output = image.copy()

    height, width, channels = output.shape
    #print height, width, channels
   

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Uses PIL to convert the grayscale image into a ndary array that ZBar can understand.
    #image = Image.fromarray(gray)
    image = np.array (gray)
    #width, height = image.size
    width = 640
    height = 360

    #Transformamos el frame para despues escanear lo que detecta
    zbar_image = zbar.Image(width, height, 'Y800', image.tostring())

    # Scans the zbar image.
    scanner = zbar.ImageScanner()
    scanner.scan(zbar_image)
    # Prints data from image.
    for decoded in zbar_image:
        #print("Data: ",decoded.data)
        #print("Tipo: ",decoded.type)
        #print("Pos: ",decoded.location)

        # Dibujando Puntos
        puntos = decoded.location
        centro = puntos[0]  
        d1 = (puntos[2][0] + puntos[3][0]) / 2
        d2 = (puntos[1][1] + puntos[2][1]) / 2

        # Centro QR Code (d1,d2)
        cv2.circle(output,(d1,d2), 5, (0,0,255), -1)

        # Centro Video Frame (c1,c2)
        c1 = 320
        c2 = 180
        cv2.circle(output,(c1,c2), 20, (0,90,255), -1)
        cv2.line(output,(c1,c2),(d1,d2),(0,0,255),5)

        print("Centro Frame :",c1, " ",c2)
        print("Centro QR code :",d1, " ",d2)
        # Movimientos
        if c1 < d1:
            print("Muevete a la derecha !!!")
        if c1 > d1:
            print("Muevete a la izquierda !!!")
        if c2 > d2:
            print("Muevete hacia arriba !!!")
        if c2 < d2:
            print("Muevete hacia abajo !!!")


       
        # Number of points in the convex hull
        n = len(puntos)
 
        # Draw the convext hull
        for j in range(0,n):
            cv2.line(output, puntos[j], puntos[ (j+1) % n], (255,0,0), 3)
            # Alineando al centro
            #if 




    
    cv2.imshow("Image", output)
    cv2.waitKey(3)


if __name__ == '__main__':
    rospy.init_node('Track')
    rospy.Subscriber("/ardrone/front/image_raw", Image, callback_image)
    rospy.spin()
   
cv2.destroyAllWindows()
