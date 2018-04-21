import numpy as np

def getRule () :
    rule_feature = [
        [ 0, 1, 1, 0],
        [ 1, 1, 1, 1],

        [ 2, 1, 2, 0],
        [ 2, 1, 1, 0],
        [ 2, 2, 1, 0],
        [ 1, 2, 1, 0],
        [ 1, 1, 2, 0],
        [ 0, 2, 1, 0],
        [ 0, 1, 1, 0],
        [ 0, 1, 2, 0],
    ]

    return rule_feature, len(rule_feature)
    