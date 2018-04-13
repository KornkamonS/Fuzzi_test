import cv2
import numpy as np
from func_feather import *
import pywt
import math
from image_func import *

def resultFeatures ( image) :
    # b, d, w_sd, w_mean, diff = [], [], [[],[],[],[]], [[],[],[],[]], []
    w_sd = []
     
    edges_g = canny_2_for_wavelet(image,'G') 

    waveLet = find_wavelet(edges_g)

    for i in range(0,4):
        waveLet[i]=(waveLet[i]-np.min(waveLet[i]))/(np.max(waveLet[i])-np.min(waveLet[i])) 
        w_sd.append(np.std(waveLet[i]))

    # water,Draw_contour,contour_result = water_edges(im,'M')

    return w_sd

