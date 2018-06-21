# import the necessary packages
import numpy as np
import argparse
import cv2
import time

def Calibrate(threshold):
    cap = cv2.VideoCapture(0) # Set Capture Device, in case of a USB Webcam try 1, or give -1 to get a list of available devices

    tryloop = 0
    found = 0
  
    cx = [0,0,0,0]
    cy = [0,0,0,0]
    

    while tryloop < 20:
        ret, frame = cap.read()

        # load the image, clone it for output, and then convert it to grayscale
        output = frame.copy()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
        # apply GuassianBlur to reduce noise. medianBlur is also added for smoothening, reducing noise.
        gray = cv2.GaussianBlur(gray,(5,5),0);
        gray = cv2.medianBlur(gray,5)
                
        # Adaptive Guassian Threshold is to detect sharp edges in the Image. For more information Google it.
        gray = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,3.5)
                
        kernel = np.ones((2.6,2.7),np.uint8)
        gray = cv2.erode(gray,kernel,iterations = 1)
        # gray = erosion
        gray = cv2.dilate(gray,kernel,iterations = 1)
        # gray = dilation

        # get the size of the final image
        # img_size = gray.shape
        # print img_size
                
        # detect circles in the image
        #circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 260, param1=30, param2=65, minRadius=0, maxRadius=0)
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 260, param1=60, param2=threshold, minRadius=0, maxRadius=0)
                
        # ensure at least some circles were found
      

        if circles is not None:
            # convert the (x, y) coordinates and radius of the circles to integers
            circles = np.round(circles[0, :]).astype("int")
            print (len(circles))
            if len(circles) >1:
                # loop over the (x, y) coordinates and radius of the circles
                c = 0
                found = 1
                for (x, y, r) in circles:
                # draw the circle in the output image, then draw a rectangle in the image
                # corresponding to the center of the circle
                    print ("C: {} \t\t X:{} \t Y:{} \t R:{}".format(c,x,y,r))
                    cx[c] = x
                    cy[c] = y
                    c = c + 1

                
                
        tryloop = tryloop + 1
        if found ==1:
            break

   

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    return found



def getCircle(threshold):
    cap = cv2.VideoCapture(0) # Set Capture Device, in case of a USB Webcam try 1, or give -1 to get a list of available devices

    tryloop = 0
    found = 0
    xt = 0
    yt = 0
    rt = 0
    x = 0
    x = 0
    r = 0 

    while tryloop < 20:
        ret, frame = cap.read()

        # load the image, clone it for output, and then convert it to grayscale
        output = frame.copy()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
        # apply GuassianBlur to reduce noise. medianBlur is also added for smoothening, reducing noise.
        gray = cv2.GaussianBlur(gray,(5,5),0);
        gray = cv2.medianBlur(gray,5)
                
        # Adaptive Guassian Threshold is to detect sharp edges in the Image. For more information Google it.
        gray = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,3.5)
                
        kernel = np.ones((2.6,2.7),np.uint8)
        gray = cv2.erode(gray,kernel,iterations = 1)
        # gray = erosion
        gray = cv2.dilate(gray,kernel,iterations = 1)
        # gray = dilation

        # get the size of the final image
        # img_size = gray.shape
        # print img_size
                
        # detect circles in the image
        #circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 260, param1=30, param2=65, minRadius=0, maxRadius=0)
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 260, param1=60, param2=threshold, minRadius=0, maxRadius=0)
                
        # ensure at least some circles were found
      

        if circles is not None:
            # convert the (x, y) coordinates and radius of the circles to integers
            circles = np.round(circles[0, :]).astype("int")
            print (len(circles))
            if len(circles) == 1:
                # loop over the (x, y) coordinates and radius of the circles
                for (x, y, r) in circles:
                # draw the circle in the output image, then draw a rectangle in the image
                # corresponding to the center of the circle
                    print ("C: {} \t\t X:{} \t Y:{} \t R:{}".format(c,x,y,r))
                    found = found+ 1
                    xt = xt + x
                    yt = yt + y
                    rt = rt + r
                
        tryloop = tryloop + 1

    if found > 2:
        x = xt / found
        y = yt / found
        r = rt / found
        print ("X:{} \t Y:{} \t R:{}".format(x,y,r))
    else:
        x = 0
        y = 0
        r = 0
        print ("No circle detected")

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    return x,y,r

