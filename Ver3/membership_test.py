import numpy as np

def getMF ():
    input_feature_top = [
            [0.3250, 0.5631, 1.8233, 1],
            [0.5631, 1.8233, 2.6188, 1],
            [1.8233, 2.6188, 4.076923077, 1]
        ],[
            [0.3226, 0.6028, 0.8677, 1],
            [0.6028, 0.8677, 1, 1]
        ],[
            [0,0.0164, 0.3462, 1],
            [0.0164, 0.3462, 0.7592, 1],
            [0.3462, 0.7592, 0.8, 1]
        ],[
            [0, 0.0010, 0.0423, 1],
            [0.0010, 0.0423, 0.0973, 1],
            [0.0423, 0.0973, 0.1, 1]
        ]
    input_feature_low = [
            [0.3250, 0.5631, 1.6666, 0.8757],
            [1.2477, 1.8233, 2.1866, 0.4567],
            [2.0877, 2.6188, 4.0769, 0.6676]
        ],[
            [0.3226, 0.6028, 0.7529, 0.5668],
            [0.7529, 0.8677, 1, 0.4332]
        ],[
            [0, 0.0164, 0.2764, 0.7882],
            [0.1103, 0.3462, 0.6416, 0.7153],
            [0.5542, 0.7592, 0.8, 0.4965]
        ],[
            [0, 0.0010, 0.0362, 0.8520],
            [0.0132, 0.0423, 0.0811, 0.7062],
            [0.0730, 0.0973, 0.1, 0.4419]
        ]
    n_rule = []
    for i in range(0,len(input_feature_top)) : 
        n_rule.append(len(input_feature_top[i]))
    return input_feature_top, input_feature_low, len(input_feature_top), n_rule

def getOutput (): 
    output_feature_top = [
        [0, 1, 2, 1],
        [1, 2, 3, 1]
    ]
    output_feature_low = [
        [0.5000, 1.0000, 1.5000, 1.0000],
        [1.5000, 2.0000, 2.5000, 1.0000]
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
