import numpy as np
from calculate_func import *
from img_func import *

def result_Feature (im) :  
    
    ### process_image ########################################
    water,Draw_contour,contour_result=water_edges(im,'M')
    edges_g = canny_2_for_wavelet(im,'M') 

    ### Calculate ###########################################
    b_result, d_result = Find_fourier(contour_result,128)  
    diff_result = Diff(water, im.copy())    
    waveLet = find_wavelet(edges_g)


    b_result=(b_result-np.min(b_result))/(np.max(b_result)-np.min(b_result))
    d_result=(d_result-np.min(d_result))/(np.max(d_result)-np.min(d_result))
    
    b_std=np.std(b_result)
    d_mean=np.mean(d_result) 

    w_sd=[]
    for i in range(0,4):
        waveLet[i]=(waveLet[i]-np.min(waveLet[i]))/(np.max(waveLet[i])-np.min(waveLet[i]))
        w_sd.append(np.std(waveLet[i]))
            
        
    return b_std , d_mean , diff_result ,w_sd[0],w_sd[1],w_sd[2],w_sd[3]
