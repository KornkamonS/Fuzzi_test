import numpy as np
from membership import getMF_v1 as getMF, getOutput, firstMem, lastMem, triangle
from rule import getRule_test_v1 as getRule
from fuzzyInterval import fuzzification, inference, outputset, outputEachRule, defuzzy, defuzzyPrint
from visualFuzz import printFuzzification, printMINIMUM_TN, printOutput
import cv2 
import sys
from result_Feature import *

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

### INIT
input_feature_top, input_feature_low, numOfFeature, n_rule = getMF()
output_feature_top, output_feature_low = getOutput()
rule_feature, numOfRule = getRule()

targetIMG = 'img//BMP_'+sys.argv[1]+'//JPCLN'+sys.argv[2]+'.bmp'
print(targetIMG)
space = 30

img = cv2.imread(targetIMG,0) 
imgRGB = cv2.imread(targetIMG,1) 
imgs = sliceIMG(img, 130, space)

len_i = np.size(imgs,0)
len_j = np.size(imgs,1)

file_name='BMP_'+sys.argv[1]+'_'+sys.argv[2]+".txt"
file = open(file_name,"w")

for i in range(0,len_i) :
    for j in range(0,len_j) :
        # input_feature = [1,1,1,1,1,1,1]
        input_feature = result_Feature(imgs[i][j])
        ##########################
        print('INPUT')
        print(input_feature)
        ##########################

        ### Fuzzification
        out_low, out_top = fuzzification(input_feature, input_feature_top, input_feature_low, numOfFeature, n_rule)
        ### Inference
        result_top, result_low, result_rule = inference(out_low, out_top, rule_feature, n_rule)
        ### Output
        result = outputEachRule (result_top, result_low, result_rule, output_feature_top, output_feature_low, 2)
        ## i,j,result
        result_print=str(i)+','+str(j)+','+str(result)+'\n'
        print(result_print,end='')
        file.write(result_print)
file.close()