import sys

import cv2
import numpy as np

from fuzzyInterval import (defuzzy, defuzzyPrint, fuzzification, inference,
                           outputEachRule, outputset)
from membership import getMF_v1 as getMF
from membership import firstMem, getOutput, lastMem, triangle
from read_result import *
from result_Feature import *
from rule import getRule_test_v1 as getRule
from visualFuzz import printFuzzification, printMINIMUM_TN, printOutput


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
def test_image(window_size,space):
    ### INIT ################################################################################
    input_feature_top, input_feature_low, numOfFeature, n_rule = getMF()
    output_feature_top, output_feature_low = getOutput()
    rule_feature, numOfRule = getRule()

    #################################################################################
    for level in range(4,6):
            with open("img//BMP_"+str(level)+"//list.txt") as f:
                fileimage = [x.strip().split('\t') for x in f.readlines()] 
            for f in fileimage:
                # print(f)
                targetIMG = "img//BMP_"+str(level)+"//"+f[0]+".bmp"           
                                
                img = cv2.imread(targetIMG,0) 
                imgs = sliceIMG(img, window_size, space)

                len_i = np.size(imgs,0)
                len_j = np.size(imgs,1)

                file_name='result//BMP_'+str(level)+'_'+f[0]+".txt"
                file = open(file_name,"w")

                for i in range(0,len_i) :
                    print(targetIMG,'runing...')
                    for j in range(0,len_j) :
                        # input_feature = [1,1,1,1,1,1,1]
                        b_std , d_mean , diff_result ,w_sd,_n__ = result_Feature(imgs[i][j])
                        result =[]
                        for k in range(0,_n__):
                            input_feature=[b_std[k],d_mean[k],diff_result[k],w_sd[k][0],w_sd[k][1],w_sd[k][2],w_sd[k][3]]
                            ##########################
                            # print('INPUT')
                            # print(input_feature)
                            ##########################
                            ### Fuzzification
                            out_low, out_top = fuzzification(input_feature, input_feature_top, input_feature_low, numOfFeature, n_rule)
                            ### Inference
                            result_top, result_low, result_rule = inference(out_low, out_top, rule_feature, n_rule)
                            ### Output
                            outputs = outputEachRule (result_top, result_low, result_rule, output_feature_top, output_feature_low, 2)
                            _result = defuzzy(outputs)
                            result.append(_result)
                        ## i,j,result ################################
                        print(result)
                        max_result=np.max(result)
                        if(max_result>0):
                            result_print=str(i)+','+str(j)+','+str(max_result)+'\n'
                            # print(result_print,end='')
                            file.write(result_print)
                        ##############################################
                file.close()

space = 50
window_size=130

# test_image(window_size,space)
show_result(0.6,space)
