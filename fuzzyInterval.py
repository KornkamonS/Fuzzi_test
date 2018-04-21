import numpy as np
from membership import firstMem, lastMem, triangle
import plotly
from plotly.graph_objs import Scatter, Layout
import plotly.graph_objs as go
from operator import itemgetter

def fuzzification(input_feature, input_feature_top, input_feature_low, numOfFeature, n_rule) :
    out_low = [] 
    out_top = []
    for i in range(0,numOfFeature) : 
        out_low.append( [] )
        out_top.append( [] )
    

    for i in range(0,numOfFeature):
        for j in range(0,n_rule[i]):
            if(j==0):
                out_top[i].append(firstMem(input_feature_top[i][j],input_feature[i]))
                out_low[i].append(firstMem(input_feature_low[i][j],input_feature[i]))
            elif(j==n_rule[i]-1):
                out_top[i].append(lastMem(input_feature_top[i][j],input_feature[i]))
                out_low[i].append(lastMem(input_feature_low[i][j],input_feature[i]))
            else:
                out_top[i].append(triangle(input_feature_top[i][j],input_feature[i]))
                out_low[i].append(triangle(input_feature_low[i][j],input_feature[i]))
    return out_low, out_top

def inference(out_low, out_top, rule_feature, n_rule) :
    result_top=[]
    result_low=[]
    result_rule=[]

    i=0
    while(i<len(rule_feature)):
        flag=True
        s_top=[]
        s_low=[]
        for j in range(0,len(rule_feature[i])-1):
            if(out_top[j][int(rule_feature[i][j])]<=0):
                flag=False
            s_top.append(out_top[j][int(rule_feature[i][j])])
            s_low.append(out_low[j][int(rule_feature[i][j])])
            
        if ( flag ): 
            result_low.append(min(s_low))
            result_top.append(min(s_top))
            result_rule.append(rule_feature[i][len(rule_feature[0])-1])
        i+=1
    return result_top, result_low, result_rule

def outputset(result_top, result_low, result_rule, n_class) :
    out = []
    for i in range(0, n_class) :
        out.append( [ [0, 1], [0, 1]])
    for i in range(0,len(result_top)) :
        for j in range(0, n_class):
            if j != result_rule[i] :
                # print(j)
                if result_top[i] > out[j][1][0] :
                    out[j][1][0] = result_top[i]
                if result_low[i] < out[j][1][1] :
                    out[j][1][1] = result_low[i]

            else :
                if result_top[i] > out[j][0][0] :
                    out[j][0][0] = result_top[i]
                if result_low[i] < out[j][0][1] :
                    out[j][0][1] = result_low[i]
    for i in range(0, n_class) :
        if out[i][0] == [0, 1] :
            out[i][0] = [0, 0]
    return out

def centroid (top, low, yORn, output_feature_top, output_feature_low) :
    yr = 0
    yl = 0
    N = 5
    x_axis = np.linspace(0,1,N)
    x_axis = x_axis[1:N-1] 
    # print(x_axis)
    y_axis_top = []
    y_axis_low = []

    # i = 0
    for x in x_axis :
        y_temp_top = 0.0
        y_temp_low = 0.0

        y_temp_top = triangle(output_feature_top[yORn] , x)
        if y_temp_top > top :
            y_axis_top.append(top)
        else : 
            y_axis_top.append(y_temp_top)
        
        y_temp_low = triangle(output_feature_low[yORn] , x)
        if y_temp_low > low :
            y_axis_low.append(0.00000000000001+low)
        else : 
            y_axis_low.append(0.00000000000001+y_temp_low)

    ### CAL YR & YL
    y = x_axis
    zeta = [y_axis_top, y_axis_low]
    num = 2**(N-2)
    bits = []
    Bcount = []
    yRL = []

    for i in range(1,num+1):
        bits.append(np.zeros(N-2))
        yRL.append(0)

    for i in range(0,N-2):
        Bcount.insert(0, (2**i) )

    for i in range(0,num):
        for j in range(0,len(bits[i])):
            if int(np.floor(i/Bcount[j])) % 2 == 1 :
                bits[i][j] = 1

    for i in range(0,num):
        for j in range(0,len(bits[i])):
            if bits[i][j] == 1 :
                bits[i][j] = zeta[0][j]
            else :
                bits[i][j] = zeta[1][j]
                
    for i in range(0,len(bits)) :
        yRL[i] = np.dot(y, bits[i]) / sum(bits[i])

    yr = max(yRL)
    yl = min(yRL)

    return yl, yr

def outputEachRule (result_top, result_low, result_rule, output_feature_top, output_feature_low, n_class) :
    # print('OUTPUT EACH RULES')
    outputs = []
    # for i in range(0, 2) :
    #     outputs.append( [] )
    for i in range(0,len(result_top)) :
        # for j in range(0, 2 ) :
            # if j == result_rule[i] :
        yl, yr = centroid(result_top[i], result_low[i], result_rule[i], output_feature_top, output_feature_low)
        outputs.append( [ result_top[i], result_low[i], yl, yr , result_rule[i] ] )
                # break
            # else : 
            #     yl, yr = centroid(result_top[i], result_low[i], 0, output_feature_top, output_feature_low)
            #     outputs[j].append( [ result_top[i], result_low[i], yl, yr , 0 ] )
                # break
        # break
    # for output in outputs :
    #     print(output)
    return outputs

def defuzzyPrint( outputs ) :
    result = []
    print('DEFUZZ')
    output = outputs
    print('==========')
    for x in output :
        print(' ' + str(x))
    outputSortedYL = output
    outputSortedYR = output

    # outputSortedYL = sorted(outputSortedYL, key=itemgetter(2))
    print(outputSortedYL)
    outputSortedYL = bubbleSort(outputSortedYL, 2)
    # outputSortedYR = sorted(outputSortedYR, key=itemgetter(3))
    outputSortedYR = bubbleSort(outputSortedYR, 3)
    print('sorted by yl')
    for x in outputSortedYL :
        print(' yl = ' + format(x[2], '.7f') + '\t' + str(x) )
    print('sorted by yr')
    for x in outputSortedYR :
        print(' yr = ' + format(x[3], '.7f') + '\t' + str(x) )
    ### YR
    print('Cal Yr')
    yr = 0
    fr = initFR(outputSortedYR)
    for i in range(0,len(fr)) :
        yr = yr + (fr[i] * outputSortedYR[i][3])  
    yr = yr /  ( sum(fr) + 0.00000000001 )
    yrI = yr
    print('FR & YR start : ' + str(fr) + ' / ' + str(yr))
    for i in range(0,len(outputSortedYR)-1):
        r = 0
        for j in range(0,len(outputSortedYR) - 1) :
            if outputSortedYR[j][3] <= yrI and yrI <= outputSortedYR[j+1][3] :
                r = j
                break
        fr = FforYR(outputSortedYR, r)
        yr = 0
        for j in range(0,len(fr)) :
            yr = yr + (fr[j] * outputSortedYR[j][3])
        yr = yr / sum(fr)
        yrII = yr
        print('FR ' + str(i) + ': ' + str(fr))
        print('R = ' + str(r))
        print('YR & YR\' & YR\'\' ' +  str(yr) + ' ' + str(yrI) + ' ' +  str(yrII))
        if yrII == yrI :
            yr = yrII
            # print('HINT YR')
            print('FINAL YR : ' + str(yr))
            break
        else :
            yrI = yrII
    print('Cal Yl')
    yl = 0
    fl = initFR(outputSortedYL)
    for i in range(0,len(fr)) :
        yl = yl + (fl[i] * outputSortedYL[i][2]) 
    yl = yl / ( sum(fl) + 0.00000000001  )
    ylI = yl
    print('FL & YL start : ' + str(fl) + ' / ' + str(yl))
    for i in range(0,len(outputSortedYL)-1) :
        l = 0
        for j in range(0,len(outputSortedYL) - 1) :
            if outputSortedYL[j][2] <= ylI and ylI <= outputSortedYL[j+1][2] :
                l = j
                break
        fl = FforYL(outputSortedYL, l)
        yl = 0
        for j in range(0,len(fl)) :
            yl = yl + (fl[j] * outputSortedYL[j][2])
        yl = yl / sum(fl)
        ylII = yl
        print('FL ' + str(i) + ': ' + str(fl))
        print('L = ' + str(l))
        print('YL & YL\' & YL\'\' ' +  str(yl) + ' ' + str(ylI) + ' ' +  str(ylII))
        if ylII == ylI :
            yl = ylII
            # print('HINT YL')s
            print('FINAL YL : ' + str(yl))
            break
        else :
            ylI = ylII
            # print(ylI)
    print('RESULT = ' + str((yr+yl)/2))
    result.append( (yr+yl)/2 )  
    return result

def defuzzy( outputs ) :
    result = 0
    output = outputs
    outputSortedYL = output
    outputSortedYR = output

    # outputSortedYL = sorted(outputSortedYL, key=itemgetter(2))
    outputSortedYL = bubbleSort(outputSortedYL, 2)
    # outputSortedYR = sorted(outputSortedYR, key=itemgetter(3))
    outputSortedYR = bubbleSort(outputSortedYR, 3)

    ### YR
    yr = 0
    fr = initFR(outputSortedYR)
    for i in range(0,len(fr)) :
        yr = yr + (fr[i] * outputSortedYR[i][3])  
    yr = yr /  ( sum(fr) + 0.00000000001 )
    yrI = yr
    for i in range(0,len(outputSortedYR)-1):
        r = 0
        for j in range(0,len(outputSortedYR) - 1) :
            if outputSortedYR[j][3] <= yrI and yrI <= outputSortedYR[j+1][3] :
                r = j
                break
        fr = FforYR(outputSortedYR, r)
        yr = 0
        for j in range(0,len(fr)) :
            yr = yr + (fr[j] * outputSortedYR[j][3])
        yr = yr / sum(fr)
        yrII = yr
        if yrII == yrI :
            yr = yrII
            break
        else :
            yrI = yrII

    yl = 0
    fl = initFR(outputSortedYL)
    for i in range(0,len(fr)) :
        yl = yl + (fl[i] * outputSortedYL[i][2]) 
    yl = yl / ( sum(fl) + 0.00000000001  )
    ylI = yl
    for i in range(0,len(outputSortedYL)-1) :
        l = 0
        for j in range(0,len(outputSortedYL) - 1) :
            if outputSortedYL[j][2] <= ylI and ylI <= outputSortedYL[j+1][2] :
                l = j
                break
        fl = FforYL(outputSortedYL, l)
        yl = 0
        for j in range(0,len(fl)) :
            yl = yl + (fl[j] * outputSortedYL[j][2])
        yl = yl / sum(fl)
        ylII = yl
        if ylII == ylI :
            yl = ylII
            break
        else :
            ylI = ylII
    result = (yr+yl)/2  
    return result

def initFR ( output ) :
    fr = []
    for out in output :
        fr.append( (out[0]+out[1]) / 2  )
    return fr

def FforYR ( output, R) :
    fr = []
    i = 0
    for out in output :
        if i <= R :
            fr.append( out[1] )
        else : 
            fr.append( out[0] )
        i = i + 1
    return fr

def FforYL ( output, L) :
    fl = []
    i = 0
    for out in output :
        if i <= L :
            fl.append( out[0] )
        else : 
            fl.append( out[1] )
        i = i + 1
    return fl

def bubbleSort(arr, key):
    arrKey = []
    for a in arr :
        arrKey.append(a[key])

    n = len(arr)
  
    for i in range(n):
        for j in range(0, n-i-1):
            if arrKey[j] > arrKey[j+1] :
                arr[j], arr[j+1] = arr[j+1], arr[j]
                arrKey[j], arrKey[j+1] = arrKey[j+1], arrKey[j]
    return arr