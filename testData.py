import numpy as np
from membership_test import getMF, getOutput, firstMem, lastMem, triangle
from rule_test import getRule
from calculate_fuzz_test import fuzzification, interface, outputset, defuzzy
import csv 

data = []
with open('data/dataCrawl.csv', 'r') as f:
    for row in csv.reader(f.read().splitlines() ):
        data.append( [] )
        for r in row :
            data[ len(data)-1 ].append( float(r) )

input_feature_top, input_feature_low, numOfFeature, n_rule = getMF()
output_feature_top, output_feature_low = getOutput()
rule_feature, numOfRule = getRule()
n_class = 5

results = []

count = [0, 0, 0, 0, 0]

for d in data :

    input_feature = d

    out_low, out_top = fuzzification(input_feature, input_feature_top, input_feature_low, numOfFeature, n_rule)

    result_top, result_low, result_rule = interface(out_low, out_top, rule_feature)

    outputs = outputset(result_top, result_low, result_rule, n_class)

    result, resultY = defuzzy(output_feature_top, output_feature_low, outputs)
    
    # results.append(result)
    xxx = []
    answer = []
    for rr in result :
        if rr > 2 :
            answer.append(1)
        else :
            answer.append(0)
        xxx.append(rr)
    index = 0
    max = 0.0
    for a in range(0, len(answer) ) :
        if answer[a] != 0.0 and resultY[a] > max :
            index = a
            max = resultY[a]
    answerSummary = np.zeros( len(answer) )
    answerSummary[index] = 1
    results.append(answerSummary) 
    if index != 2 :
        print('---------->' + str(xxx) + '->' + str(index+1) )
    else :
        print(str(xxx) + '->' + str(index+1))
    count[index] = count[index] + 1
    # print(str(input_feature) + '->' + str( np.where(answerSummary == 1) ) )

# for r in results :
#     print(r)

print(count)

# print(float(data[0][0]))
# print(' ')
# print(data[0])
# print(data[0][0])