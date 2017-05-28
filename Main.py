import cv2
import numpy as np
import Conversion
from math import *
import ArduinoControl

camerastats = {'bottomFOV': 16, 'middleFOV':55, 'cameraHeight': 76, 'focalLength':0.3, 'pixelHeight': 2448, 'pixelWidth': 3264}
cap = cv2.VideoCapture('white.mp4')

while 1:
    ret, frame = cap.read()
    img = frame[300:540, 200:760]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7, 7), 0)
    edges = cv2.Canny(blur, 50, 150, apertureSize=3)

    #detect all lines and create 2 empty lists for right and left line
    lines = cv2.HoughLinesP(edges, 0.8, np.pi/180, 100, np.array([]), minLineLength=50, maxLineGap=200)
    right = []
    left = []

#separating lines by slope
    if lines is None:
        print("No worries")
    else:
        for x1,y1,x2,y2 in lines[:, 0]:
            if x2 - x1 == 0.:  # corner case, avoiding division by 0
                m = 999.  # practically infinite slope
            else:
                m = (y2-y1)/(x2-x1) #rise over run
                if m > 0:
                    right.append([x1, y1, x2, y2])
                    cv2.line(img, (x1,y1), (x2, y2), (0, 0, 255), 2)
                else:
                    left.append([x1, y1, x2, y2])
                    cv2.line(img, (x1,y1), (x2, y2), (255, 0, 0), 2)

        right_mask = cv2.inRange(img, (0,0,220), (0,0,255))
        left_mask = cv2.inRange(img, (240, 0, 0), (255, 0, 0))

    right_line = cv2.HoughLines(right_mask, 1, np.pi / 180, 200)
    if right_line is None:
        print("no worries")
    else:
        for rho, theta in right_line[0]:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))

            cv2.line(img, (x1, y1), (x2, y2), (100, 255, 0), 10)

            realx1, realy1 = Conversion.real_slope(y1, x1, camerastats)
            realx2, realy2 = Conversion.real_slope(y2, x2, camerastats)
            real_right_slope = (realy2 - realy1) / (realx2 - realx1)

    left_line = cv2.HoughLines(left_mask, 1, np.pi / 180, 200)
    if left_line is None:
        print("no worries")
    else:
        for rho, theta in left_line[0]:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))

            cv2.line(img, (x1, y1), (x2, y2), (0,255,100),10)

            realx1, realy1 = Conversion.real_slope(y1,x1, camerastats)
            realx2, realy2 = Conversion.real_slope(y2, x2, camerastats)
            real_left_slope = (realy2 - realy1)/(realx2 - realx1)

    right_degrees = math.atan(real_right_slope)
    left_degrees = math.atan(real_left_slope)

    direction = ArduinoControl.servo_mtr(right_degrees, left_degrees)
    ArduinoControl.motor(right_degrees,left_degrees,direction)

    cv2.imshow('img', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()