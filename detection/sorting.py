# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 15:09:40 2023

@author: Owner
"""
import numpy as np
import cv2
import os.path
from os import path
from PIL import Image
from PIL import ImageDraw
from PIL import ImageOps
from shapely.geometry import Polygon, Point

remove_list = ['\n']
coordinate_list = []

def get_box_precedence(box, cols, factor):
    tolerance_factor = factor
    b1 = int(box[1])
    b0 = int(box[0])
    return ((b1 // tolerance_factor) * tolerance_factor) * cols + b0


def sorting(box, column):
    rmax = 0
    rmin = 2000000
    max_height = 0
    
    for j in box:
        j = j.split(',')    # 구분을 위한 ',' 을 제거
        j[7] = j[7].replace('\n', '')   # y4 값 뒤에 붙어있는 개행문자를 제거
        rmax = max(rmax, int(j[2]), int(j[4]))
        rmin = min(rmin, int(j[0]), int(j[6]))
        max_height = max(max_height, abs(int(j[1]) - int(j[5])), abs(int(j[1]) - int(j[7])), abs(int(j[3]) - int(j[5])), abs(int(j[3]) - int(j[7])))
        coordinate_list.append(j)
        
    sorted_list = sorted(coordinate_list, key=lambda x: get_box_precedence(x, column, max_height))
    print(sorted_list)
    
    
    return sorted_list, rmax, rmin