# importing the modules
import cv2
import numpy as np

# set Width and Height of output Screen
frameWidth = 1080
frameHeight = 720

# capturing Video from Webcam
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

# set brightness, id is 10 and
# value can be changed accordingly
cap.set(20, 150)

# object color values
myColors = [[5, 107, 0, 19, 255, 255],
            [133, 56, 0, 159, 156, 255],
            [57, 76, 0, 100, 255, 255],
            [90, 48, 0, 118, 255, 255]]

# color values which will be used to paint
# values needs to be in BGR
myColorValues = [[51, 153, 255],
                 [255, 0, 255],
                 [0, 255, 0],
                 [255, 0, 0]]

# [x , y , colorId ]
myPoints = []

# Function to display color and coordinates on the frame


def displayInfo(frame, point, color):
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 0.5
    fontColor = (255, 255, 255)
    lineType = 2

    text = f"Color: {color}, Coordinates: ({point[0]}, {point[1]})"
    cv2.putText(frame, text, (10, 30), font, fontScale, fontColor, lineType)

# Function to pick color of object


def findColor(img, myColors, myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints = []

    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x, y = getContours(mask)

        cv2.circle(imgResult, (x, y), 15, myColorValues[count], cv2.FILLED)
        if x != 0 and y != 0:
            newPoints.append([x, y, count])
        count += 1
    return newPoints

# Contours function used to improve accuracy of paint


def getContours(img):
    contours, hierarchy = cv2.findContours(
        img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    x, y, w, h = 0, 0, 0, 0

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x + w // 2, y

# Draws your action on the virtual canvas


def drawOnCanvas(myPoints, myColorValues):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]),
                   10, myColorValues[point[2]], cv2.FILLED)


# Running infinite while loop
while True:
    success, img = cap.read()
    imgResult = img.copy()

    # Finding the colors for the points
    newPoints = findColor(img, myColors, myColorValues)
    if len(newPoints) != 0:
        for newP in newPoints:
            myPoints.append(newP)

    if len(myPoints) != 0:
        # Drawing the points
        drawOnCanvas(myPoints, myColorValues)

        # Displaying color and coordinates on the frame
        for point in myPoints:
            displayInfo(
                imgResult, (point[0], point[1]), myColorValues[point[2]])

    # Displaying output on screen
    cv2.imshow("Result", imgResult)

    # Condition to break program's execution
    # Press 'q' to stop the execution of the program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
