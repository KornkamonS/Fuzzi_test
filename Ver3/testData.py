import numpy as np
from membership_test import getMF, getOutput, firstMem, lastMem, triangle
from rule_test import getRule
from fuzzyInterval import fuzzification, inference, outputset, outputEachRule, defuzzy, defuzzyPrint
from visualFuzz import printFuzzification, printMINIMUM_TN, printOutput
import csv 
fileTarget = 'dataRun'
data = []
with open('../data/' + fileTarget +'.csv', 'r') as f:
    for row in csv.reader(f.read().splitlines() ):
        data.append( [] )
        for r in row :
            data[ len(data)-1 ].append( float(r) )

results = []
class_results = []
count = [0, 0, 0, 0, 0]

### INIT
input_feature_top, input_feature_low, numOfFeature, n_rule = getMF()
output_feature_top, output_feature_low = getOutput()
rule_feature, numOfRule = getRule()
n_class = 5
###

cccc = 1
for d in data :

    input_feature = d

    out_low, out_top = fuzzification(input_feature, input_feature_top, input_feature_low, numOfFeature, n_rule)
    result_top, result_low, result_rule = inference(out_low, out_top, rule_feature)
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
    # results.append(answerSummary) 
    results.append(input) 
    class_results.append(index+1)
    if index != 0 :
        print(str(cccc) + ' ' + '---------->' + str(input) + '->' + str(index+1) )
    else :
        print(str(cccc) + ' ' + str(input) + '->' + str(index+1))
    count[index] = count[index] + 1
    cccc = cccc + 1

print(count)

file = open('result' + fileTarget + '.txt','w') 
j = 0
for result in results :
    for i in range(0,len(result)) :
        file.write(str(result[i]) + ',' )
    file.write(str(class_results[j]) + '\n')
    j = j + 1
file.close() 

