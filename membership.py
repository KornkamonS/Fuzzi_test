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
