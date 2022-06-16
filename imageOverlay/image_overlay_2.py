
#from os import startfile
from pickle import NONE
import cv2
import numpy as np
import copy
import subprocess

from torch import double
 
def on_mouse(event, x, y, flag, param):        
    global rect, rects
    global leftButtonDowm
    global leftButtonUp
    global cap
    global frame_count
    global step
    global img0, img
    global end_frame

    if event == cv2.EVENT_LBUTTONDOWN:
        rect[0] = x
        rect[2] = x
        rect[1] = y
        rect[3] = y
        leftButtonDowm = True
        leftButtonUp = False

    if event == cv2.EVENT_MOUSEMOVE:
        if leftButtonDowm and  not leftButtonUp:
            rect[2] = x
            rect[3] = y        

    if event == cv2.EVENT_LBUTTONUP:
        if leftButtonDowm and  not leftButtonUp:
            x_min = min(rect[0], rect[2])
            y_min = min(rect[1], rect[3])
            x_max = max(rect[0], rect[2])
            y_max = max(rect[1], rect[3])
            rect[0] = x_min
            rect[1] = y_min
            rect[2] = x_max
            rect[3] = y_max
            leftButtonDowm = False      
            leftButtonUp = True 

            # roi = img[rect[1]:(rect[3] + 1), rect[0]:(rect[2] + 1)]
            # img0[rect[1]:(rect[3] + 1), rect[0]:(rect[2] + 1)] = roi
            print(" ")
            for i in range(x_min, x_max, 1):
                for j in range(y_min, y_max, 1):
                    should_replace = True
                    for rct in rects:
                        if isInRect(i, j, rct):
                            print(str(i) + " and " + str(j) + " in [" + str(rct[0]) + ", " + str(rct[1]) + ", " + str(rct[2]) + ", " + str(rct[3]) + "] ")
                            should_replace = False
                            break

                    if should_replace:
                        print("replace")
                        img0[j, i] = img[j, i]

            rects.append(copy.deepcopy(rect))
            cv2.imshow('out', img0)
            for i in range(step):
                if frame_count >= end_frame:
                    print("Finished!")
                    cv2.imwrite('real_exp_8/out.png', img0)
                    exit()
                _, img = cap.read()
                frame_count += 1
            cv2.imshow('img', img)

def getRectIntersection(rect1, rect2):
    if (rect1[0] > rect2[2] or rect1[1] > rect2[3] or 
        rect2[0] > rect1[2] or rect2[1] > rect1[3]):
        return None
    else:
        rect = [0, 0, 0, 0]
        rect[0] = max(rect1[0], rect2[0])
        rect[1] = max(rect1[1], rect2[1])
        rect[2] = min(rect1[2], rect2[2])
        rect[3] = min(rect1[3], rect2[3])

        return rect

def isInRect(x, y, rctg):
    return (x >= rctg[0] and x < rctg[2] and 
            y >= rctg[1] and y <= rctg[3])

video_path='real_exp_8/real_exp_8_2.mp4'

cap=cv2.VideoCapture(video_path)

thresh = 65
step = 50

frame_num=cap.get(cv2.CAP_PROP_FRAME_COUNT)


start_frame = int((11.0 / 40.0) * frame_num)
end_frame = int((24.0 / 40.0) * frame_num)

weight = 0.7

frame_count = 0
for i in range(start_frame + 1):
    _, img0 = cap.read()
    frame_count += 1
print(frame_count)

rect = [0,0,0,0]  
rects = []
last_rect = rect
leftButtonDowm = False
leftButtonUp = True
cv2.namedWindow('out')
cv2.imshow('out', img0)
_, img = cap.read()
cv2.namedWindow('img') 
cv2.setMouseCallback('img',on_mouse)
cv2.imshow('img', img)
frame_count += 1

cv2.waitKey()

