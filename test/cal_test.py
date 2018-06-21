import numpy as np
import cv2

#pts1 = np.float32([[462,342],[460,123],[124,99],[115,363]])
pts1 = np.float32([[342,462],[123,460],[99,124],[363,115]])
pts2 = np.float32([[200.3643,-86.2533],[301.4947,-76.5043],[302.8254,79.8156],[185.2143,86.2132]])

#M = cv2.getAffineTransform(pts1,pts2)
M = cv2.getPerspectiveTransform(pts1,pts2)
print (M)

point = [302,79,0]
x,y,z = M.dot(point)

print (x,y)
