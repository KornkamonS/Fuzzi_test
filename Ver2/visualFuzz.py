import numpy as np

def printFuzzification (out_low, out_top) :
    print('OUT LOW')
    for i in range(0,len(out_low)) :
        print(str(i) + ' : ' + str(out_low[i]))
    print('OUT TOP')
    for i in range(0,len(out_top)) :
        print(str(i) + ' : ' + str(out_top[i]))

def printMINIMUM_TN (result_top, result_low, result_rule) : 
    print('MINIMUM T-NORM')
    for i in range(0,len(result_top)) :
        print('hint ' + str(result_rule[i]) + ' : [' + str(result_top[i]) + ' ' + str(result_low[i]) + ']')

def printOutput (outputs) :
    print('FIRES OUTPUT SETS WITH MINIMUM T-NORM [ Yes, No ]')
    for i in range(0,len(outputs)) :
        print('class' + str(i) + ' :'+ str(outputs[i][0]) )
        print('\t' + str(outputs[i][1]) )