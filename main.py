import cv2 as cv
import numpy as np
import sys
from sliceIMG import sliceIMG
from resultFeathers import resultFeatures
from membership import getMF, getOutput, firstMem, lastMem, triangle, getMF_WSD
from rule1 import getRule
from fuzzyInterval import fuzzification, inference, outputset, outputEachRule, defuzzy, defuzzyPrint

# print('Hello ')

targetIMG = '/Users/mac/Google Drive/Project/DB/All247images/Benign/' + sys.argv[1] + '/BMP/JPCLN' + sys.argv[2] + '.bmp'
# targetIMG = '/Users/mac/Google Drive/Project/DB/All247images/Malignant/' + sys.argv[1] + '/BMP/JPCLN' + sys.argv[2] + '.bmp'
print(targetIMG)
space = 10
img = cv.imread(targetIMG,0) 
imgRGB = cv.imread(targetIMG,1) 
imgs = sliceIMG(img, 130, space)
len_i = np.size(imgs,0)
len_j = np.size(imgs,1)

input_feature_top, input_feature_low, numOfFeature, n_rule = getMF_WSD()
output_feature_top, output_feature_low = getOutput()
rule_feature, numOfRule = getRule()
n_class = 5

for i in range(0,len_i) :
    for j in range(0,len_j) :
        # print(imgs[i][j])
        print( (i * len_j ) + j )
        # print(resultFeatures(imgs[i][j]))
        xxxxxxxx = str(resultFeatures(imgs[i][j]))
        input_fuzzy = resultFeatures(imgs[i][j])
        if ~np.isnan(np.sum(input_fuzzy)) :
            ### Fuzzification
            out_low, out_top = fuzzification(input_fuzzy, input_feature_top, input_feature_low, numOfFeature, n_rule)
            ### Inference
            result_top, result_low, result_rule = inference(out_low, out_top, rule_feature)
            ### Output
            outputs = outputEachRule (result_top, result_low, result_rule, output_feature_top, output_feature_low, n_class)
            result = defuzzy(outputs)
            # print(result)
            xxxxxxxx = xxxxxxxx + ' ----> ' +str(result[0])
            yyyy = (result[0] - 2) * 10000
            if yyyy < 0 :
                yyyy = 0.0
            if result[0] > 2.1 :
                cv.rectangle(imgRGB, (j*space,i*space), ((j*space)+130,(i*space)+130), (0,0,255), 2)
            print(xxxxxxxx)


cv.imshow('img',img)
cv.imshow('xxxx',imgRGB)

cv.waitKey(0)
cv.destroyAllWindows()