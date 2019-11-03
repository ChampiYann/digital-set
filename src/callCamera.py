import cv2
import numpy as np
from pprint import pprint

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    #-----Converting image to LAB Color model----------------------------------- 
    lab= cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    # cv2.imshow("lab",lab)

    #-----Splitting the LAB image to different channels-------------------------
    l, a, b = cv2.split(lab)
    # cv2.imshow('l_channel', l)
    # cv2.imshow('a_channel', a)
    # cv2.imshow('b_channel', b)

    #-----Applying CLAHE to L-channel-------------------------------------------
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(10,10))
    cl = clahe.apply(l)
    # cv2.imshow('CLAHE output', cl)

    #-----Merge the CLAHE enhanced L-channel with the a and b channel-----------
    limg = cv2.merge((cl,a,b))
    # cv2.imshow('limg', limg)

    #-----Converting image from LAB Color model to RGB model--------------------
    final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    # cv2.imshow('final', final)

    gray = cv2.cvtColor(final,cv2.COLOR_BGR2GRAY)
    gray,thresh1 = cv2.threshold(gray,160,255,cv2.THRESH_BINARY)
    gray = np.float32(thresh1)

    contours,hirerarchy = cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    # Display the resulting frame
    rects = [cv2.minAreaRect(contour) for contour in contours]
    boxes = [cv2.boxPoints(rect) for rect in rects]
    boxes = np.int0(boxes)
    areas = [cv2.contourArea(box) for box in boxes]

    # Scan rectangles for for the ones looking like cards
    cardIDs = [i for i in range(len(contours)) if areas[i] >= 5000]
    cards = boxes[cardIDs]

    # print([len([hire for hire in hirerarchy[0] if hire[3] == j]) for j in cardIDs])

    cv2.drawContours(frame,cards,-1,(255,0,255),2)

    cv2.imshow('frame',frame)
    cv2.imshow('gray',gray)
    if cv2.waitKey(1) & 0xFF == 27:
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()


