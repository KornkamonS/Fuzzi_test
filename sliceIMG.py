import cv2
import numpy as np

def sliceIMG(img, size_windown, space) :
    img_output = []
    height, width = img.shape
    index_Y = 0
    while index_Y + size_windown <= height :
        index_X = 0
        img_output.append( [] )
        while index_X + size_windown <= width :
            img_output[len(img_output)-1].append( img[index_Y: index_Y + 130, index_X: index_X + 130]  )
            index_X = index_X + space
            # print(index_X, index_Y)
        index_Y = index_Y + space
    return img_output
