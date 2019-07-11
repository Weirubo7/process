import os
import cv2
import numpy as np
from process.write_xml import *
import json

# 用来处理百视泰最新图像，规格：1936*256

def process(imgPath):
    savePath = 'E:/Panji_SampleSpace/merge_data'

    image = cv2.imread(imgPath)
    imageName = imgPath.split('/')[-1]
    classNum = imgpath.split('/')[-2]
    height, width = image.shape[0:2]
    xmlPath = imgPath[0:-4] + '.xml'
    saveDir = savePath + '/' + classNum
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)

    bboxes = get_bbox(read_xml(xmlPath))
    num = 1

    for box in bboxes:

        xmin, ymin, xmax, ymax = box

        borderL, borderR = get_border(image)
        borderT, borderB = 0, height

        box_length = height
        if xmax - xmin < 100 and ymax - ymin < 100:
            box_length = 200
            
        xmid, ymid = int((xmin + xmax) / 2), int((ymin + ymax) / 2)

        # 左上角
        xlt = xmid - int(box_length / 2)
        ylt = 0

        # 右下角
        xrb = xlt + box_length
        yrb = ylt + box_length

        # 边界处理
        if(xlt < borderL):
            xlt = borderL
            xrb = xlt + box_length
        if(xrb > borderR):
            xrb = borderR
            xlt = xrb - box_length

        try:
            image_roi = image[ylt:yrb, xlt:xrb]
            # cv2.rectangle(image, (xlt, ylt), (xrb, yrb), (0, 255, 0), 2)
            # cv2.imwrite('1.jpg', image)
            image_roi = cv2.resize(image_roi, (299,299))
            dst = saveDir + '/' + imageName[:-4] + '_' + str(num) + '.jpg'
            cv2.imwrite(dst, image_roi)
        except:
            print(imageName + ": error occur!")


# 处理图像背景黑图,寻找背景和有钢部分边界
def get_border(img):
    # imgPath = 'data/SIS01/SIS01_1261_10_0078.jpg'
    # img = cv2.imread(imgPath)
    height, width = img.shape[0:2]

    # 计算sobel并二值化
    # x = cv2.Sobel(img, cv2.CV_16S, 1, 0)
    # absX = cv2.convertScaleAbs(x)  # 转回uint8
    # _, thresh = cv2.threshold(absX, 1, 128, cv2.THRESH_BINARY)
    # thresh_col = np.sum(thresh, 0)[:, 0]
    # cv2.imwrite('1.jpg', absX)

    # 计算灰度值
    gray_col = np.sum(img, 0)[:, 0] / height # 取一个通道
    gray_max = max(gray_col)

    border_l, border_r = 0, width
    # print(gray_col[1680:1750])

    for i in range(10, len(gray_col)-10):
        # 左右各取10列通过灰度判断是否为边界
        gray_l = gray_col[i-10:i].sum() / 10
        gray_r = gray_col[i:i+10].sum() / 10
        if gray_r - gray_l > 20 and gray_l < gray_max * 0.3:
            border_l = i + 7
            border_r = width
            break
        elif gray_l - gray_r > 20 and gray_r < gray_max * 0.3:
            border_l = 0
            border_r = i - 5
            break

    # for i in range(len(gray_col)-1):
    #     # 边界要同时满足灰度阈值和sobel阈值
    #     if gray_col[i+1] - gray_col[i] > 15:
    #         border_l = i
    #         border_r = width
    #         break
    #     elif gray_col[i] - gray_col[i+1] > 15:
    #         border_l = 0
    #         border_r = i
    #         break

    # cv2.rectangle(img, (border_l, 0), (border_r, height), (0,255,0), 2)
    # cv2.imwrite('2.jpg', img)

    return border_l, border_r

if __name__ == '__main__':
    # imgpath = 'data/SIS01_1066_12_0101.jpg'
    # xmlpath = 'data/SIS01_1066_12_0101.xml'
    # dst = 'data'
    # # process(imgpath, xmlpath, dst)
    #
    # img = cv2.imdecode(np.fromfile(imgpath, dtype=np.uint8), -1)
    # bboxs = get_bbox(read_xml(xmlpath))
    #
    # for bbox in bboxs:
    #     # img_roi = img[bbox[1]:bbox[3], bbox[0]:bbox[2]]
    #     center_x, center_y = int((bbox[2] + bbox[0]) / 2), int((bbox[3] + bbox[1]) / 2)
    #     img_roi = img[center_y-75:center_y+75, center_x-75:center_x+75]
    #     img_roi = cv2.resize(img_roi, (299, 299))
    #     cv2.imwrite('data/b.jpg', img_roi)

    # path = 'data/SIS01'
    # for file in os.listdir(path):
    #     if '.jpg' in file:
    #         imgpath = path + '/' + file
    #         process(imgpath)

    # process('data/SIS01/SIS01_1318_07_6649.jpg')
    imgpath = 'E:/Panji_SampleSpace/panji_data/4/sis_1219_04_0013_1.jpg'
    process(imgpath)



