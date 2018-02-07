# from pylab import *
import numpy as np
# import matplotlib.pyplot as plt
from membership_test import getMF, getOutput, firstMem, lastMem, triangle
from rule_test import getRule
from fuzzyInterval import fuzzification, inference, outputset, outputEachRule, defuzzy
from visualFuzz import printFuzzification, printMINIMUM_TN, printOutput
import csv 

data = []
with open('../data/dataCar.csv', 'r') as f:
    for row in csv.reader(f.read().splitlines() ):
        data.append( [] )
        for r in row :
            data[ len(data)-1 ].append( float(r) )

results = []
count = [0, 0, 0, 0, 0]

input_feature_top, input_feature_low, numOfFeature, n_rule = getMF()
output_feature_top, output_feature_low = getOutput()
rule_feature, numOfRule = getRule()
n_class = 5

# input_feature=[0.711538462,	0.903846154,	0,	0.1]
# input_feature = [0.884615385,	0.807692308,	0.02,	0.1]
# input_feature = [1.733333333,	0.966666667,	0.14,	0.1]
cccc = 1
for d in data :

    input_feature = d

    out_low, out_top = fuzzification(input_feature, input_feature_top, input_feature_low, numOfFeature, n_rule)
    ####
    # printFuzzification(out_low, out_top)
    ####
    result_top, result_low, result_rule = inference(out_low, out_top, rule_feature)
    # result_top_inverse = 1-np.array(result_top)
    # result_low_inverse = 1-np.array(result_low)
    ####
    # printMINIMUM_TN(result_top, result_low, result_rule )
    # printMINIMUM_TN(1-np.array(result_top), 1-np.array(result_low), result_rule )
    #####

    # outputEachRule(result_top, result_low, result_rule, output_feature_top, output_feature_low, n_class)

    # ####
    # outputs = outputset(result_top, result_low, result_rule, n_class)
    # ####
    # printOutput(outputs)
    # ####

    # result = defuzzy(output_feature_top, output_feature_low, outputs)

    outputs = outputEachRule (result_top, result_low, result_rule, output_feature_top, output_feature_low, n_class)
    result = defuzzy(outputs)

    input = []
    answer = []
    for rr in result :
        if rr > 1 :
            answer.append(1)
        else :
            answer.append(0)
        input.append(rr)
    index = 0
    max = 0.0
    for a in range(0, len(answer) ) :
        if answer[a] != 0.0 and result[a] > max :
            index = a
            max = result[a]
    answerSummary = np.zeros( len(answer) )
    answerSummary[index] = 1
    results.append(answerSummary) 
    if index != 0 :
        print(str(cccc) + ' ' + '---------->' + str(input) + '->' + str(index+1) )
    else :
        print(str(cccc) + ' ' + str(input) + '->' + str(index+1))
    count[index] = count[index] + 1
    cccc = cccc + 1
    # if cccc == 632 :
    #     break
print(count)