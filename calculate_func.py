import numpy as np
import cv2
import math
import pywt
from decimal import Decimal
def Find_fourier(testContour,slicing):
    if(len(testContour)<slicing):
        return [0],[0]
    ####### FOURIER
    dis = int(len(testContour) / slicing)
    edgesFourier = []
    x, y = [], []
    for j in range (0,slicing ) :
        x.append(testContour[j*dis][0][1])
        y.append(testContour[j*dis][0][0])
        edgesFourier.append(complex(testContour[j*dis][0][1], testContour[j*dis][0][0]))
    fft = np.fft.fft(edgesFourier)
    magnitude = []
    for ff in fft :
        magnitude.append( math.sqrt((ff.real*ff.real) + (ff.imag*ff.imag)) )
    b = []
    d = []
    for j in range(0,len(magnitude)-1) :
        b.append( float(Decimal(( magnitude[ j+1 ]*magnitude[ j-1 ]) ) / Decimal((magnitude[1]*magnitude[1])) ))
        d.append( float(Decimal(Decimal(magnitude[ j+1 ]) * Decimal(pow(Decimal(magnitude[1]),j)) ) / Decimal((pow(Decimal(magnitude[1]),j+1)) ) ))
    b.append( float(( magnitude[ 0 ]*magnitude[ len(magnitude) - 1 - 1 ] ) / (magnitude[1]*magnitude[1]) ))
    d.append( float((Decimal(magnitude[ 0 ]) * Decimal(pow(Decimal(magnitude[1]),len(magnitude) - 1) )) / (Decimal(pow(Decimal(magnitude[1]),len(magnitude) - 1 + 1))) ))
    # print(b,d)
    return b,d
    ######
def find_wavelet(thresh):
    coeffs = pywt.dwt2(thresh, 'db10')
    cA, (cH, cV, cD) = coeffs
    return [cA.flatten(), cH.flatten(), cV.flatten(), cD.flatten()]
def Diff(thresh,imgCopy):
    # imgCopy=cv2.cvtColor(imgCopy,cv2.COLOR_BGR2GRAY)
    mask = thresh
    in_obj = cv2.bitwise_and(imgCopy,imgCopy, mask= mask)
    area_in = np.sum(mask) / np.max(mask)

    mask = np.max(thresh) - thresh
    out_obj = cv2.bitwise_and(imgCopy,imgCopy, mask= mask)
    area_out = np.sum(mask) / np.max(mask)

    if area_in == imgCopy.shape[0]*imgCopy.shape[1] :
        diff = 0
    else :
        diff = (np.sum(in_obj)/area_in ) - ( (np.sum(out_obj)/area_out ) )

    return diff
