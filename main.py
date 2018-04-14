import cv2 as cv
import numpy as np
import sys
from sliceIMG import sliceIMG
from resultFeathers import resultFeatures
from membership import getMF, getOutput, firstMem, lastMem, triangle, getMF_WSD
from rule1 import getRule
from fuzzyInterval import fuzzification, inference, outputset, outputEachRule, defuzzy, defuzzyPrint

# print('Hello ')

targetIMG = '/Users/mac/Documents/Semester2-2017/Fuzzi_test/IMG/JPCLN' + sys.argv[1] + '.bmp'
# targetIMG = '/Users/mac/Google Drive/Project/DB/All247images/Benign/' + sys.argv[1] + '/BMP/JPCLN' + sys.argv[2] + '.bmp'
# targetIMG = '/Users/mac/Google Drive/Project/DB/All247images/Malignant/' + sys.argv[1] + '/BMP/JPCLN' + sys.argv[2] + '.bmp'
print(targetIMG)
space = 10
img = cv.imread(targetIMG,0) 
imgRGB = cv.imread(targetIMG,1) 
# imgs = sliceIMG(img, 130, space)
# len_i = np.size(imgs,0)
# len_j = np.size(imgs,1)

input_feature_top, input_feature_low, numOfFeature, n_rule = getMF_WSD()
output_feature_top, output_feature_low = getOutput()
rule_feature, numOfRule = getRule()
n_class = 2

height, width = img.shape
index_Y = 0
black = np.zeros( (2048,2048), np.uint8 )


size_windown = 130
while index_Y + size_windown <= height :
    index_X = 0
    while index_X + size_windown <= width :
        target = img[index_Y: index_Y + 130, index_X: index_X + 130]
        input_fuzzy = resultFeatures(target)
        xxxxxxxx = str(input_fuzzy)
        if ~np.isnan(np.sum(input_fuzzy)) :
            ## Fuzzification
            out_low, out_top = fuzzification(input_fuzzy, input_feature_top, input_feature_low, numOfFeature, n_rule)
            ### Inference
            result_top, result_low, result_rule = inference(out_low, out_top, rule_feature)
            ### Output
            outputs = outputEachRule (result_top, result_low, result_rule, output_feature_top, output_feature_low, n_class)
            result = defuzzy(outputs)
            if result[1] > 1.9 and result[0] < 1.1  :
                xxxxxxxx = xxxxxxxx + ' ----> ' +str(result)
                black[index_Y: index_Y + 130, index_X: index_X + 130] = img[index_Y: index_Y + 130, index_X: index_X + 130]
                cv.rectangle(imgRGB, (index_X,index_Y), ((index_X)+130,(index_Y)+130), (0,0,255), 2)
                print(  str(index_X) + ',' + str(index_Y) + ' ' + str(xxxxxxxx))

        index_X = index_X + space
        # print(index_X, index_Y)
    index_Y = index_Y + space

# for i in range(0,len_i) :
#     for j in range(0,len_j) :
#         # print(imgs[i][j])
#         # print( (i * len_j ) + j )
#         # print(resultFeatures(imgs[i][j]))
#         xxxxxxxx = str(resultFeatures(imgs[i][j]))
#         input_fuzzy = resultFeatures(imgs[i][j])
#         if ~np.isnan(np.sum(input_fuzzy)) :
#             ### Fuzzification
#             out_low, out_top = fuzzification(input_fuzzy, input_feature_top, input_feature_low, numOfFeature, n_rule)
#             ### Inference
#             result_top, result_low, result_rule = inference(out_low, out_top, rule_feature)
#             ### Output
#             outputs = outputEachRule (result_top, result_low, result_rule, output_feature_top, output_feature_low, n_class)
#             result = defuzzy(outputs)
#             # print(result)
#             xxxxxxxx = xxxxxxxx + ' ----> ' +str(result)
#             # Detect
#             if result[1] > 1.9 and result[0] < 1.1  :
#                 print( (i * len_j ) + j )
#                 cv.rectangle(imgRGB, (j*space,i*space), ((j*space)+130,(i*space)+130), (0,0,255), 2)
#                 cv.rectangle(imgRGB, (i*space,j*space), ((i*space)+130,(j*space)+130), (255,0,0), 2)
#                 black[]
#                 print(xxxxxxxx)


cv.imshow('img',img)
cv.imshow('black',black)
cv.imshow('imgRGB',imgRGB)

cv.waitKey(0)
cv.destroyAllWindows()