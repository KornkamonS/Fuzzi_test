import numpy as np
from membership_test import getMF, getOutput, firstMem, lastMem, triangle
from rule_test import getRule
from fuzzyInterval import fuzzification, inference, outputset, outputEachRule, defuzzy, defuzzyPrint
from visualFuzz import printFuzzification, printMINIMUM_TN, printOutput

### INIT
input_feature_top, input_feature_low, numOfFeature, n_rule = getMF()
output_feature_top, output_feature_low = getOutput()
rule_feature, numOfRule = getRule()
n_class = 5
###

input_feature=[0.711538462, 0.903846154, 0, 0.1]
# input_feature = [1.342105263,	0.973684211,	0.12,	0.1]
# input_feature = [0.638554217,	0.987951807,	0,	0.1]
# input_feature = [0.648648649,	0.567567568,	0,	0]
# input_feature = [2.777777778, 0.833333333, 0.52, 0.045]

##########################
print('INPUT')
print(input_feature)
##########################

### Fuzzification
out_low, out_top = fuzzification(input_feature, input_feature_top, input_feature_low, numOfFeature, n_rule)
printFuzzification(out_low, out_top)
### Inference
result_top, result_low, result_rule = inference(out_low, out_top, rule_feature)
printMINIMUM_TN(result_top, result_low, result_rule )
### Output
outputs = outputEachRule (result_top, result_low, result_rule, output_feature_top, output_feature_low, n_class)
result = defuzzyPrint(outputs)
print(' ')
print(result)