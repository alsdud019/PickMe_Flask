# -*- coding: utf-8 -*-
"""
Created on Mon May  1 13:17:12 2023

@author: Owner
"""
import numpy as np
import cv2
import os.path
import sorting
from os import path
from PIL import Image
from PIL import ImageDraw
from PIL import ImageOps
from shapely.geometry import Polygon, Point

#img_root = './test/'
img_root = './static/'
#box_root = './result/'
box_root = './detection/result/'

remove_list = {'\n'}
spaceimg = []
coordinate_list = []

pts = np.zeros((4, 2), dtype=np.float32)

extensions = ['.gif', '.jpg', '.jpeg', '.png']



def cropping(filename, file_ext):
    """
    valid_extension = ""
    
    for ext in extensions:
        if os.path.isfile(filename + ext):
            valid_extension = valid_extension + ext
            break
        
    
    print("\n ext is : " + valid_extension)
    """
    
    
    if file_ext == '.jpg' or file_ext == '.jpeg' or file_ext == '.PNG' or file_ext =='.gif' or file_ext == '.png':
        
        print("\n\n")
        print("파일명 : " + filename +"\n")
        print("파일 확장자 : " + file_ext+"\n")
        
        print("파일명 + 파일 확장자 : " + filename + file_ext + "\n")
        print("경로 + 파일 : " + img_root + filename + file_ext + "\n")
        
        print(path.exists(img_root + filename + file_ext))
        
        img = Image.open(img_root+filename+file_ext)
        imag = cv2.imread(img_root+filename+file_ext)
        rows, cols = imag.shape[:2]
        
        box = open(box_root + 'res_' + filename +'.txt', 'r')   # bounding box가 저장된 txt 파일
    
        lines = box.readlines()
        lines = [ i for i in lines if i not in remove_list] # 가독성을 위해 추가되어있는 개행문자들을 제거
        
        coordinate, max_x, min_x = sorting.sorting(lines, imag.shape[1])
        
        """
        for j in lines:
            j = j.split(',')    # 구분을 위한 ',' 을 제거
            j[7] = j[7].replace('\n', '')   # y4 값 뒤에 붙어있는 개행문자를 제거
            for i in range(0, len (j), 2):
                coordinate_list.append([j[i],j[i+1]])
                
        """
        for j in coordinate:
            for i in range(0, len(j), 2):
                coordinate_list.append([j[i],j[i+1]])
        
        
        
        #print(coordinate_list[0])
        index = 0
        for i in range(0, len(coordinate_list), 4):
            x1 = int(coordinate_list[i][0]) # (x1, y1) : 좌상단
            y1 = int(coordinate_list[i][1])
            x2 = int(coordinate_list[i+1][0])   # (x2, y2) : 우상단
            y2 = int(coordinate_list[i+1][1])
            x3 = int(coordinate_list[i+2][0])   # (x3, y3) : 우하단
            y3 = int(coordinate_list[i+2][1])
            x4 = int(coordinate_list[i+3][0])   # (x4, y4) : 좌하단
            y4 = int(coordinate_list[i+3][1])
            
            
            pts[0] = [x1,y1]
            pts[1] = [x2,y2]
            pts[2] = [x3,y3]
            pts[3] = [x4,y4]
            
            if len(pts) == 4:
                # 좌표 4개 중 상하좌우 찾기
                sm = pts.sum(axis=1)  # 4쌍의 좌표 각각 x+y 계산
                diff = np.diff(pts, axis=1)  # 4쌍의 좌표 각각 x-y 계산
    
                topLeft = pts[np.argmin(sm)]  # x+y가 가장 값이 좌상단 좌표
                bottomRight = pts[np.argmax(sm)]  # x+y가 가장 큰 값이 우하단 좌표
                topRight = pts[np.argmin(diff)]  # x-y가 가장 작은 것이 우상단 좌표
                bottomLeft = pts[np.argmax(diff)]  # x-y가 가장 큰 값이 좌하단 좌표
    
                # 변환 전 4개 좌표 
                pts1 = np.float32([topLeft, topRight, bottomRight, bottomLeft])
    
                # 변환 후 영상에 사용할 서류의 폭과 높이 계산
                w1 = abs(bottomRight[0] - bottomLeft[0])
                w2 = abs(topRight[0] - topLeft[0])
                h1 = abs(topRight[1] - bottomRight[1])
                h2 = abs(topLeft[1] - bottomLeft[1])
                width = int(max([w1, w2]))  # 두 좌우 거리간의 최대값이 서류의 폭
                height = int(max([h1, h2]))  # 두 상하 거리간의 최대값이 서류의 높이
    
                # 변환 후 4개 좌표
                pts2 = np.float32([[0, 0], [width - 1, 0],
                                   [width - 1, height - 1], [0, height - 1]])
    
                # 변환 행렬 계산 
                mtrx = cv2.getPerspectiveTransform(pts1, pts2)
                # 원근 변환 적용
                result = cv2.warpPerspective(imag, mtrx, (width, height))
                
                pre_file_name = filename+'_{:03}.png'.format(index)   # 파일명_번호 로 저장
                
                cv2.imwrite('./recog/demo_korean/9th/pre/' + pre_file_name, result)
                
                threshold = 25
                
                if abs(max_x - max(x2,x3)) < threshold or abs(min(x1, x4) - min_x) < 25:
                    if index != 0:
                        spaceimg.append(result)
                    
                if len(spaceimg) > 1:
                    min_height = min(img.shape[0] for img in spaceimg)
                    resized_images = [cv2.resize(img, (img.shape[1], min_height)) for img in spaceimg]
                    combined_image = np.hstack(resized_images)
                    combined_name = 'combined' + '_{:03}.png'.format(index)
                    
                    cv2.imwrite('./recog/demo_korean/9th/pre/' + combined_name, combined_image)
                    spaceimg.clear()

            index = index + 1
            
        coordinate_list.clear()
        coordinate.clear()
        
    
    
    else:
        print("지원하는 확장자가 아닙니다.")
