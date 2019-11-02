import cv2
import numpy as np
from pprint import pprint

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # frame = cv2.GaussianBlur(frame,(5,5),0)
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray,thresh1 = cv2.threshold(gray,130,255,cv2.THRESH_BINARY)

    gray = np.float32(thresh1)

    contours,hirerarchy = cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


    # dst = cv2.cornerHarris(gray,4,5,0.04)

    #result is dilated for marking the corners, not important
    # dst = cv2.dilate(dst,None)

    # Threshold for an optimal value, it may vary depending on the image.
    # frame[dst>0.01*dst.max()]=[0,0,255]

    # Display the resulting frame
    topLevel = [i for i, x in enumerate(hirerarchy[0]) if x[3]==-1]
    countChildren = [hirerarchy for i in topLevel]

    # for cnts in contours:
    cv2.drawContours(frame,[contours[i] for i in topLevel],-1,(255,0,255),2)

    cv2.imshow('frame',frame)
    cv2.imshow('gray',gray)
    if cv2.waitKey(1) & 0xFF == 27:
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()


