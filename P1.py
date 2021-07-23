import cv2
import numpy as np

# Draw on screen with air pens and webcam

cap = cv2.VideoCapture(-1) # 0 should work, but sometimes fails on linux
cap.set(3,640)
cap.set(4,480)
cap.set(10,150)

myColors = [[  0,  90, 184,  42, 247, 255],     # Orange
            [161, 133, 156, 179, 255, 255],     # Red
            [  0, 198, 193, 179, 255, 255],     # Blue
            [113, 106, 192, 157, 220, 255],     # purple
            [ 36, 145, 141, 110, 255, 255]]     # green - last color clears the drawn points

myColorValues = [[ 51, 153, 255],                #BBGR
                 [  0,   0, 255],
                 [255,   0,   0],
                 [255,   0, 200],
                 [100, 255,   0]]

clearColor = [ 36, 145, 141, 110, 255, 255]

myPoints = []

def findColor(img):
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    for count, color in enumerate(myColors):
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x, y = getContours(mask)
        if x > 0 and y > 0 and count + 1 == len(myColors):
            myPoints.clear()
        elif x != 0 and y != 0:
            myPoints.append([x,y,count])

def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE) #cv2.CHAIN_APPROX_SIMPLE

    x, y, w, h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 300:
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            x,y,w,h = cv2.boundingRect(approx)
    return x+w//2, y+h//2

def drawOnCanvas():
    for point in myPoints:
        cv2.circle(imgResult, (point[0],point[1]), 10, myColorValues[point[2]], cv2.FILLED)

while True:
    success, img = cap.read()
    imgResult = img.copy()

    findColor(img )
    drawOnCanvas()
    imgResult = cv2.resize(imgResult, (0,0), None,  2, 2)
    cv2.imshow("Image",imgResult)

    if cv2.waitKey(1) != -1:
        cv2.destroyAllWindows()
        break
