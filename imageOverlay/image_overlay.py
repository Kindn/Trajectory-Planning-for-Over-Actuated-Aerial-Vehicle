
#from os import startfile
import cv2
import numpy as np
import subprocess

from torch import double
 
 
video_path='real_exp_8/real_exp_8_2.mp4'

cap=cv2.VideoCapture(video_path)

thresh = 65
step = 20

frame_count=cap.get(cv2.CAP_PROP_FRAME_COUNT)

_, img0 = cap.read()
img0_gray = cv2.cvtColor(img0,cv2.COLOR_BGR2GRAY)

img_out = img0

start_frame = 11.0 / 40.0
end_frame = 24.0 / 40.0

weight = 0.7
i0 = 0
i0_set = False

for i in range(int(frame_count - 1)):#逐帧抓取图片
    _,img = cap.read()
    
    if i / frame_count >= start_frame and i / frame_count <= end_frame:
        if not i0_set:
            i0 = i
            i0_set = True
        if (i - i0) % step == 0:
            img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)   #cv2.COLOR_RGB2HSV     cv2.COLOR_BGR2GRAY
            h, w = img_gray.shape
            print(img_gray.shape)
            for row in range(h):
                for col in range(w):
                    if np.abs(int(img_gray[row, col]) - int(img0_gray[row, col])) > thresh:
                        img_out[row, col] = img[row, col] * weight + img0[row, col] * (1.0 - weight)
            cv2.imshow("out", img_out)
            cv2.waitKey(5)

            proc_rate = (i - i0) / ((end_frame - start_frame) * frame_count)
            print("\rprocessing..." + str(proc_rate * 100) + "%")

cv2.imshow("out", img_out)
cv2.imwrite("real_exp_8/out.jpg", img_out)
print("Image saved.")
cv2.waitKey()

