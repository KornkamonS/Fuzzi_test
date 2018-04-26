import numpy as np
from calculate_func import *
from image_func import *

def resultFeature_multi (im) :
    ### Process image ###################################
    water,Draw_contour,contour_result,__n__ = multiple_water(im,'M')
    # edges_g = canny_2_for_wavelet(im,'M') 

    ### Calcalate Feature #######################################
    b_std,b_mean,d_std,d_mean,diff_result,w_std,w_mean =[],[],[],[],[],[],[]
    for i in range(__n__):
        b,d = Find_fourier(contour_result[i],32)  
        diff = Diff(water[i], im.copy())
        
        diff_result.append(diff)

        b_mean.append(np.mean(b)) 
        d_std.append(np.std(d))      

    
    return b_mean , d_std , diff_result  , __n__
