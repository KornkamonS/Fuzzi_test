# from pylab import *
import numpy as np
# import matplotlib.pyplot as plt
from membership_test import getMF, getOutput, firstMem, lastMem, triangle
from rule_test import getRule
from calculate_fuzz_test import fuzzification, interface, outputset, defuzzy

input_feature_top, input_feature_low, numOfFeature, n_rule = getMF()
output_feature_top, output_feature_low = getOutput()
rule_feature, numOfRule = getRule()
n_class = 5

input_feature=[0.711538461538462, 0.903846153846154, 0, 0.100000000000000]
out_low, out_top = fuzzification(input_feature, input_feature_top, input_feature_low, numOfFeature, n_rule)

result_top, result_low, result_rule = interface(out_low, out_top, rule_feature)

outputs = outputset(result_top, result_low, result_rule, n_class)

defuzzy(output_feature_top, output_feature_low, outputs)