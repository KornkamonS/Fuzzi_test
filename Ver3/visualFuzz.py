import numpy as np

def printFuzzification (out_low, out_top) :
    print('OUT LOW / OUT TOP')
    for i in range(0,len(out_low)) :
        # format(a, '.2f')
        low = '[ '
        top = '[ '
        for j in out_low[i] : 
            low = low + format(j, '.2f') + ' '
        for m in out_top[i] : 
            top = top + format(m, '.2f') + ' '
        low = low + ']'
        top = top + ']'
        print(str(i) + ' : ' + low + '\t/ ' + top)

def printMINIMUM_TN (result_top, result_low, result_rule) : 
    print('MINIMUM T-NORM')
    for i in range(0,len(result_top)) :
        print('hint ' + str(result_rule[i]) + ' : [' + str(result_top[i]) + ' ' + str(result_low[i]) + ']')

def printOutput (outputs) :
    print('FIRES OUTPUT SETS WITH MINIMUM T-NORM [ Yes, No ]')
    for i in range(0,len(outputs)) :
        print('class' + str(i) + ' :'+ str(outputs[i][0]) )
        print('\t' + str(outputs[i][1]) )