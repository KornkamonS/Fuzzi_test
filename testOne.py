import numpy as np
from membership import getMF, getOutput, firstMem, lastMem, triangle
# from rule1 import getRule
from rule import getRule
from fuzzyInterval import fuzzification, inference, outputset, outputEachRule, defuzzy, defuzzyPrint
from visualFuzz import printFuzzification, printMINIMUM_TN, printOutput

### INIT
input_feature_top, input_feature_low, numOfFeature, n_rule = getMF()
output_feature_top, output_feature_low = getOutput()
rule_feature, numOfRule = getRule()

input_feature = [188.34572678331091, 0.070879107560830129, 0.017604697787453501]

##########################
print('INPUT')
print(input_feature)
##########################

### Fuzzification
out_low, out_top = fuzzification(input_feature, input_feature_top, input_feature_low, numOfFeature, n_rule)
printFuzzification(out_low, out_top)
### Inference
result_top, result_low, result_rule = inference(out_low, out_top, rule_feature, n_rule)
printMINIMUM_TN(result_top, result_low, result_rule )
### Output
outputs = outputEachRule (result_top, result_low, result_rule, output_feature_top, output_feature_low, 2)
# for x in outputs :
#     print(x)
result = defuzzyPrint(outputs)
print(' ')
print(result)