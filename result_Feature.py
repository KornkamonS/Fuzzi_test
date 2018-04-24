import numpy as np
from calculate_func import *
from img_func import *

def result_Feature (im) :  
    
    ### Process image ###################################
    water,_,contour_result,_n__=multiple_water(im,'M')
    # edges_g = canny_2_for_wavelet(im,'M') 

    ### Calcalate Feature #######################################
    b_std=[] 
    d_mean=[]
    diff_result=[]
    waveLet=[]
    w_sd=[]
    for i in range(_n__):
        b,d = Find_fourier(contour_result[i],128)        
        diff = Diff(water[i], im.copy())
        _wavelet = find_wavelet(water[i]) 
        # waveLet.append(_wavelet) 
        # b_result.append(b)
        # d_result.append(d)
        
        diff_result.append(diff)

        # b=(b-np.min(b))/(np.max(b)-np.min(b))
        # d=(d-np.min(d))/(np.max(d)-np.min(d))

        b_std.append(np.std(b))
        d_mean.append(np.mean(d)) 

        w_sd.append([])
        for j in range(0,4):
            tmp=(_wavelet[j]-np.min(_wavelet[j]))/(np.max(_wavelet[j])-np.min(_wavelet[j]))
            w_sd[i].append(np.std(tmp))


    # print('*****************************')
    # print(b_std,d_mean,sep='\n')
    # print(diff_result) 
    # for i in range(_n__):
    #     print(w_sd[i])
        
    return b_std , d_mean , diff_result ,w_sd,_n__
