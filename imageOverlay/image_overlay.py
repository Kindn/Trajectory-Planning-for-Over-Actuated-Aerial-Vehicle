
import cv2
import numpy as np
import subprocess
 
 
video_path='test_env_2_exp_2/video.mp4'

cap=cv2.VideoCapture(video_path)

thresh = 10
step = 10

frame_count=cap.get(cv2.CAP_PROP_FRAME_COUNT)

_, img0 = cap.read()
img0_gray = cv2.cvtColor(img0,cv2.COLOR_BGR2GRAY)

img_out = img0

for i in range(int(frame_count - 1)):#逐帧抓取图片
    _,img = cap.read()
    
    if i % step == 0:
        #img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)   #cv2.COLOR_RGB2HSV     cv2.COLOR_BGR2GRAY
        h, w, _ = img.shape
        for row in range(h):
            for col in range(w):
                delta = img[row, col] - img0[row, col]
                if np.linalg.norm(delta) > thresh:
                    img_out[row, col] = img[row, col]

        print(str(i) + "/" + str(frame_count))

cv2.imshow("out", img_out)
cv2.imwrite("test_env_2_exp_2/out.jpg", img_out)
cv2.waitKey()

