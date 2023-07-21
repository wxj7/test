# -*- coding: utf-8 -*-
"""
@Time ： 2023/7/11 14:15
@Auth ： wxj
@File ：count.py
@IDE ：PyCharm
"""

import cv2
import numpy as np
def detect_open(source):
    img=cv2.imread(source,1) #读取图片
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #将图片变为灰度图片
    kernel=np.ones((2,2),np.uint8) #进行腐蚀膨胀操作
    erosion=cv2.erode(gray,kernel,iterations=5) #腐蚀
    dilation=cv2.dilate(erosion,kernel,iterations=5) #膨胀
    ret, thresh = cv2.threshold(dilation, 150, 255, cv2.THRESH_BINARY) # 阈值处理 二值法
    thresh1 = cv2.GaussianBlur(thresh,(3,3),0)# 高斯滤波
    thresh2 = cv2.medianBlur(thresh,3,0)#中值滤波
    contours,hirearchy=cv2.findContours(thresh2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)# 找出连通域

    #对连通域面积进行比较
    area=[] #建立空数组，放连通域面积
    contours1=[]   #建立空数组，放减去最小面积的数
    for i in contours:
          # area.append(cv2.contourArea(i))
          # print(area)
         if cv2.contourArea(i)>30:  # 计算面积 去除面积小的 连通域
            contours1.append(i)
    sum=len(contours1)-1
    print(sum) #计算连通域个数
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img,'sum='+str(sum),(0,50), font, 1, (200,255,155), 2, cv2.LINE_AA)
    draw=cv2.drawContours(img,contours1,-1,(0,255,0),1) #描绘连通域
    # cv2.imwrite(r"D:\maixin\result_col\1.jpg",draw)
    # cv2.imwrite(r"D:\maixin\result_col\thresh2.jpg",thresh2)
    # cv2.imwrite(r"D:\maixin\result_col\thresh.jpg",thresh)
    # cv2.imwrite(r"D:\maixin\result_col\gray.jpg",gray)

    #求连通域重心 以及 在重心坐标点描绘数字
    for i,j in zip(contours1,range(len(contours1))):
        M = cv2.moments(i)
        cX=int(M["m10"]/M["m00"])
        cY=int(M["m01"]/M["m00"])
        draw1=cv2.putText(draw, str(j), (cX, cY), 1,1, (255, 0, 255), 1) #在中心坐标点上描绘数字
    cv2.imwrite(r"D:\maixin\result_col\draw1.jpg",draw1)
    #cv2.imshow("draw1",draw1)
    cv2.imshow("draw",draw)
    cv2.imshow("thresh1",thresh1)
    cv2.imshow("gray",gray)
    cv2.imshow("thresh2",thresh2)
    cv2.imshow("thresh",thresh)


    cv2.waitKey()
    cv2.destroyWindow()
source="E:\\Maixin\\dualstain\\yolov5\\data\\coltest\\colony2.png"
detect_open(source)
