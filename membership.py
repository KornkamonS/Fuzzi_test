import numpy as np

def getMF ():
    input_feature_top = [
            [0, 150, 180, 1],
            [140, 170 , 200, 1],
            [190, 240, 255, 1]
        ],[
            [0.0, 0.055, 0.08, 1],
            [0.055, 0.075, 0.095, 1],
            [0.07, 0.09, 0.15, 1]
        ],[
            [0,0.010, 0.0155, 1],
            [0.005, 0.015, 0.025, 1],
            [0.015, 0.025, 0.05, 1]
        ]
    input_feature_low = [
            [0, 150, 165, 0.8],
            [155, 170, 185, 0.8],
            [205, 240, 255, 0.8]
        ],[
            [0.0, 0.055, 0.075, 0.8],
            [0.06, 0.075, 0.09, 0.8],
            [0.075, 0.09, 0.15, 0.8]
        ],[
            [0, 0.010, 0.0145, 0.7],
            [0.01, 0.015, 0.02, 0.9],
            [0.02, 0.025, 0.05, 0.7]
        ]
    n_rule = []
    for i in range(0,len(input_feature_top)) : 
        n_rule.append(len(input_feature_top[i]))
    return input_feature_top, input_feature_low, len(input_feature_top), n_rule

def getOutput (): 
    output_feature_top = [
        [0, 0.25, 0.5, 1],
        [0.25, 0.5, 1, 1]
    ]
    output_feature_low = [
        [0.125, 0.25, 0.375, 1],
        [0.625, 0.5, 1, 1]
    ]
    return output_feature_top, output_feature_low

def triangle(fuzzi,x) :
    [ b, m, d, h ] = fuzzi
    M = 0
    if ( x >= b and x <= m) :
        M = ( (0-h)/(b-m) ) * ( x - b )
    if ( x > m and x <= d ):
        M = h + ( h/(m-d) ) * ( x - m )
    return M

def firstMem(fuzzi,x):
    [ b, m, d, h ] = fuzzi
    M = 0
    if ( x <= m ):
        M = h
    if ( x > m and x <= d ):
        M = h + ( h/(m-d) ) * ( x-m )
    return M

def lastMem(fuzzi,x):
    [ b, m, d, h ] = fuzzi
    M = 0
    if ( x >= b and x <= m):
        M = ( (0-h)/(b-m) ) * ( x-b )
    if (x > m  and x <= d):
        M = h
    return M
def getMF_v1():
    input_feature_top = [ #b
            [0.00000000 , 0.08869 , 0.10553714, 1],
            [0.097 , 0.11120529 , 0.117959, 1],
            [0.115696 , 0.122489 , 0.12525 , 1],
            [0.1223239 , 0.126758 , 0.30000000, 1]
        ],[#d
            [0.00000000 , 0.0136745 , 0.0152728, 1],
            [0.014644 , 0.0161636 , 0.018, 1],
            [0.0173427 , 0.0185742 , 0.0197009, 1],
            [0.019072 , 0.0205961 , 0.1, 1]
        ],[#diff
            [-20 , 5.2095, 9.7622, 1],
            [7.9753 ,11.58,12.5073, 1],
            [11.58 , 16.5073, 22.0262, 1],
            [18.1393 , 23.3747, 80, 1]
        ],[#ca
            [0.00000000 , 0.069136, 0.101722, 1],
            [0.0932881 , 0.1040220, 0.11878, 1],
            [0.11054 , 0.133925, 0.140442, 1],
            [0.1368 , 0.144468, 0.30000000, 1]
        ],[#ch
            [0.00000000 , 0.037607, 0.07, 1],
            [0.0637107 , 0.0720964, 0.094413, 1],
            [0.0915727 , 0.095, 0.20000000, 1]
        ],[#cv
            [0.00000000 , 0.0328, 0.045924, 1],
            [0.0350782 , 0.06399, 0.0653608, 1],
            [0.0631176 , 0.06699808, 0.070844, 1],
            [0.0686009 , 0.0725887, 0.0886364, 1],
            [0.0775735 , 0.089762, 0.20000000, 1]
        ],[#cd
            [0.00000000 , 0.0319, 0.0546435, 1],
            [0.0445798 , 0.0613729, 0.067977, 1],
            [0.06561 , 0.0669808, 0.07121791, 1],
            [0.0684763 , 0.0723395, 0.0850506, 1],
            [0.0831814 , 0.0880415, 0.20000000, 1]
        ]
    input_feature_low = [#b
            [0.00000000 , 0.08869 , 0.097, 0.4],
            [0.10553714 , 0.11120529 , 0.11120529, 0.5],
            [0.117959 , 0.122489 , 0.12525 , 1],
            [0.126758 , 0.126758 , 0.30000000, 0.8]
        ],[  #d
            [0.00000000 , 0.0136745 , 0.014644, 1],
            [0.0152728 , 0.0161636 , 0.0173427, 1],
            [0.018 , 0.0185742 , 0.019072, 1],
            [0.0197009 , 0.0205961 , 0.1, 1]
        ], [#diff
            [-20 , 5.2095, 7.9753, 1],
            [9.7622 ,11.58,11.58, 1],
            [12.5073 , 16.5073, 18.1393, 1],
            [22.0262 , 23.3747, 80, 1]
        ],[#ca
            [0.00000000 , 0.069136, 0.0720113, 1],
            [0.101722 , 0.104022, 0.11054, 0.8],
            [0.11878 , 0.133925, 0.1368, 0.8],
            [0.140442 , 0.144468, 0.3, 1]
        ],[#ch
            [0.00000000 , 0.037607, 0.0637107, 0.8],
            [0.07 , 0.0720964, 0.0915727, 1],
            [0.094413 , 0.095, 0.20000000, 1]
        ],[#cv
            [0.00000000 , 0.0328, 0.0350782, 0.8],
            [0.045924 , 0.06399, 0.0631176, 0.4],
            [0.0653608  , 0.06699808, 0.0686009, 1],
            [0.070844 , 0.0725887, 0.0775735, 1],
            [0.0886364 , 0.089762, 0.20000000, 0.5]
        ],[#cd
            [0.00000000 , 0.0319, 0.0445798, 1],
            [0.0546435 , 0.0613729, 0.06561, 0.6],
            [0.067977 , 0.0669808, 0.0684763, 1],
            [0.07121791  , 0.0723395, 0.0831814, 1],
            [0.0850506  , 0.0880415, 0.20000000, 1]
        ]
    n_rule = []
    for i in range(0,len(input_feature_top)) : 
        n_rule.append(len(input_feature_top[i]))
    return input_feature_top, input_feature_low, len(input_feature_top), n_rule