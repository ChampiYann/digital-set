import cv2
import numpy as np

img = cv2.imread('./img/cards1.jpg',0)
_,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
_,th2 = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)
_,th3 = cv2.threshold(img,127,255,cv2.THRESH_TRUNC)
_,th4 = cv2.threshold(img,127,255,cv2.THRESH_TOZERO)
_,th5 = cv2.threshold(img,127,255,cv2.THRESH_TOZERO_INV)
while(True):
    cv2.imshow('image',img)
    cv2.imshow('bin',th1)
    cv2.imshow('tozero',th4)
    cv2.imshow('tozeroinv',th5)
    if cv2.waitKey(1) & 0xFF == 27:
        break


cv2.waitKey(0)
cv2.destroyAllWindows()
