import sys

import cv2
import numpy as np

from fuzzyInterval import (defuzzy, defuzzyPrint, fuzzification, inference,
                           outputEachRule, outputset)

from membership import getMF,getOutput,getRule
from read_result import show_result
from result_Feature import resultFeature_multi
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

    test_file=["img//Train//nodule//","img//Train//none//"]
    nodule=['nodule','none']
    #################################################################################
    for level in range(2):
        with open(test_file[level]+'list.txt') as f:
            fileimage = [x.strip().split('\t') for x in f.readlines()] 
        for f in fileimage:
            targetIMG = test_file[level]+f[0]+".bmp"           
            print(targetIMG)                     
            img = cv2.imread(targetIMG,0) 
            imgs = sliceIMG(img, window_size, space)

            len_i = np.size(imgs,0)
            len_j = np.size(imgs,1)

            file_name='result//'+nodule[level]+'//'+f[0]+".txt"
            file = open(file_name,"w")

            for i in range(len_i) :
                print(targetIMG,'runing...')
                for j in range(len_j) :
                    b_mean , d_std , diff_result ,_n__ = resultFeature_multi(imgs[i][j])
                    result =[]
                    for k in range(_n__):
                        input_feature=[b_mean[k],d_std[k],diff_result[k]]
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
                    # print(result)
                    max_result=np.max(result)                        
                    if(max_result>0.0):
                        result_print=str(i)+','+str(j)+','+str(max_result)+'\n'
                        file.write(result_print)
                            ##############################################
            file.close()
def save_roc(window_size,space):
    ### save roc curve
    file_name='result//roc_curve.txt'
    file = open(file_name,'w')
    file.write('cut-off,True_positive,False_positive\n')
    _list=np.arange(0,1.1,0.1,dtype='float')
    # print(_list)
    for i in _list:
        print(i)
        n_tp,n_fp = show_result(i,space,window_size)
        file.write(str(i)+','+str(n_tp)+','+str(n_fp)+'\n')
    file.close()
space = 30
window_size=130

test_image(window_size,space)
# show_result(0.8,space,window_size)

print('----------  finish!!!!!!!!!!  ------------------')
## BMP008 finish