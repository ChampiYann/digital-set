import cv2
import numpy as np
from pprint import pprint
from statistics import mean

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # frame = cv2.imread('.\set.jpg')

    #-----Converting image to LAB Color model----------------------------------- 
    lab= cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)

    #-----Splitting the LAB image to different channels-------------------------
    l, a, b = cv2.split(lab)

    #-----Applying CLAHE to L-channel-------------------------------------------
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(10,10))
    cl = clahe.apply(l)

    #-----Merge the CLAHE enhanced L-channel with the a and b channel-----------
    limg = cv2.merge((cl,a,b))

    #-----Converting image from LAB Color model to RGB model--------------------
    final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    # Convert contrast increased image to HSV
    hsv = cv2.cvtColor(final, cv2.COLOR_BGR2HSV)
    # Split the channels
    h, s, v = cv2.split(hsv)
    
    # Shift hue to remove the rd color from the weird 0-360 overlap
    shiftAngle = 90
    _,hueAdditionMask = cv2.threshold(h,180-shiftAngle,255,cv2.THRESH_BINARY)
    cv2.add(h, -(180-shiftAngle), h, mask=hueAdditionMask)
    cv2.add(h, shiftAngle, h, mask=cv2.bitwise_not(hueAdditionMask))

    # Convert contrasted frame to grayscale
    gray = cv2.cvtColor(final,cv2.COLOR_BGR2GRAY)
    # set threshold
    _,thresh1 = cv2.threshold(gray,160,255,cv2.THRESH_BINARY)
    gray = np.float32(thresh1)
    # find the contours
    contours,hirerarchy = cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    # Make rectangles of the contours
    rects = [cv2.minAreaRect(contour) for contour in contours]
    boxes = [cv2.boxPoints(rect) for rect in rects]
    boxes = np.int0(boxes)
    # Find size of boxes
    areas = [cv2.contourArea(box) for box in boxes]

    # Scan rectangles for for the ones looking like cards
    cardIDs = [i for i in range(len(contours)) if areas[i] > 3000 and hirerarchy[0][i][3] == -1]
    cards = boxes[cardIDs]

    # Find the number of elements big enough to be a symbol inside a card and their contour indexes
    numElem = [len([i for i in range(len(contours)) if hirerarchy[0][i][3] == j and areas[i] > 500]) for j in cardIDs]
    symbolIDs = [[i for i in range(len(contours)) if hirerarchy[0][i][3] == j and areas[i] > 500] for j in cardIDs]

    # create a mask of the contours
    contourMask = np.zeros_like(h)
    cv2.drawContours(contourMask, [contours[i] for symbol in symbolIDs for i in symbol], -1, color=255, thickness=-1)
    _,contourMask = cv2.threshold(contourMask,127,255,cv2.THRESH_BINARY)

    # Normalize the hue map for the contours
    hNorm = h.copy()
    cv2.normalize(h,hNorm,0,255,norm_type=cv2.NORM_MINMAX,mask=cv2.bitwise_and(cv2.bitwise_not(thresh1),contourMask))
    # Normalize the saturation map for the contours
    sNorm = s.copy()
    cv2.normalize(s,sNorm,0,255,norm_type=cv2.NORM_MINMAX,mask=cv2.bitwise_and(cv2.bitwise_not(thresh1),contourMask))

    # cv2.imshow('aNorm',cv2.bitwise_and(aNorm,aNorm,mask=cv2.bitwise_and(cv2.bitwise_not(thresh1),contourMask)))
    # cv2.imshow('hNorm',cv2.bitwise_and(hNorm,hNorm,mask=cv2.bitwise_and(cv2.bitwise_not(thresh1),contourMask)))
    # cv2.imshow('sNorm',cv2.bitwise_and(sNorm,sNorm,mask=cv2.bitwise_and(cv2.bitwise_not(thresh1),contourMask)))


    satMean = []
    hueMean = []
    # Loop over the cards
    for symbolIDsCard in symbolIDs:
        satMeanCard = []
        hueMeanCard = []
        # Loop over the symbols on the cards
        for symbolID in symbolIDsCard:
            # draw the contours on the frame
            cv2.drawContours(frame,[contours[symbolID]],-1,255,1)
            # Create a mask of the contours of the symbol
            contourMask = np.zeros_like(h)
            cv2.drawContours(contourMask, [contours[symbolID]], -1, color=255, thickness=-1)
            _,contourMask = cv2.threshold(contourMask,127,255,cv2.THRESH_BINARY)
            # narrow the mask to remove white, this leaves only the part with color
            mask = cv2.bitwise_and(contourMask,cv2.bitwise_not(thresh1))
            # find the mean of the saturation
            meanSat,stdDevSat = cv2.meanStdDev(sNorm,mask=mask)
            satMeanCard.append(meanSat[0,0])
            # find the mena of the hue
            meanHue,stdDevHue = cv2.meanStdDev(hNorm,mask=mask)
            hueMeanCard.append(meanHue[0,0])
        # average for all symbols on the card since they are the same color
        try:
            satMean.append(mean(satMeanCard))
        except:
            satMean.append(0)

        try:
            hueMean.append(mean(hueMeanCard))
        except:
            hueMean.append(0)

    # draw the card contours on the frame
    cv2.drawContours(frame,cards,-1,255,2)

    # Loop over the cards
    for i in range(len(cardIDs)):
        # Get the moments of the card
        M = cv2.moments(cards[i])
        # calculate the center point of the card
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        # write the number of symbols on the card
        cv2.putText(frame,str(numElem[i]),(cx,cy),cv2.FONT_HERSHEY_SIMPLEX,1.0,(255,0,255),2)
        # find the color of the symbols
        # purple empty symbols and purple half filled symbol are almost black and their saturation is thus low
        if satMean[i] < 20:
            cv2.putText(frame,"purple",(cx,cy+30),cv2.FONT_HERSHEY_SIMPLEX,1.0,(255,0,255),2)
        elif hueMean[i] > 105 and hueMean[i] < 150:
            cv2.putText(frame,"red",(cx,cy+30),cv2.FONT_HERSHEY_SIMPLEX,1.0,(255,0,255),2)
        elif hueMean[i] > 190:
            cv2.putText(frame,"green",(cx,cy+30),cv2.FONT_HERSHEY_SIMPLEX,1.0,(255,0,255),2)
        elif hueMean[i] < 100:
            cv2.putText(frame,"purple",(cx,cy+30),cv2.FONT_HERSHEY_SIMPLEX,1.0,(255,0,255),2)
        else:
            cv2.putText(frame,"unknown",(cx,cy+30),cv2.FONT_HERSHEY_SIMPLEX,1.0,(255,0,255),2)

    # show the frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break
    # cv2.waitKey()

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()