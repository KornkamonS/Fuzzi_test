import numpy as np
from membership_test import firstMem, lastMem, triangle
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

def inference(out_low, out_top, rule_feature) :
    result_top=[]
    result_low=[]
    result_rule=[]

    i=0
    while(i<len(rule_feature)):
        flag=True
        s_top=[]
        s_low=[]
        for j in range(0,len(rule_feature[i])-1):
            if(rule_feature[i][j]==-1):
                for kk in range(0,n_rule[j]):
                    temp_rule=[]
                    for k in range(0,len(rule_feature[i])):                    
                        if(k==j):
                            temp_rule.append(kk)
                        else:
                            temp_rule.append(rule_feature[i][k])
                    rule_feature.append(temp_rule)
                    flag=False                 
                break           
            elif(out_top[j][int(rule_feature[i][j])]<=0):
                flag=False
            s_top.append(out_top[j][int(rule_feature[i][j])])
            s_low.append(out_low[j][int(rule_feature[i][j])])
    
        if(flag): 
            result_low.append(min(s_low))
            result_top.append(min(s_top))
            result_rule.append(rule_feature[i][len(rule_feature[3])-1])
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
    if yORn == 1 :
        x_axis = np.linspace(1,3,201)
    else :
        x_axis = np.linspace(0,2,201)
    y_axis_top = []
    y_axis_low = []
    y_axis_top_X = []
    y_axis_low_X = []
    i = 0
    for x in x_axis :
        y_temp_top = 0.0
        y_temp_low = 0.0

        y_temp_top = triangle(output_feature_top[yORn] , x)
        if y_temp_top > top :
            y_axis_top.append(top)
        else : 
            y_axis_top.append(y_temp_top)
        y_axis_top_X.append(y_axis_top[i] * x)
        
        y_temp_low = triangle(output_feature_low[yORn] , x)
        if y_temp_low > low :
            y_axis_low.append(low)
        else : 
            y_axis_low.append(0.00000000001+y_temp_low)
        y_axis_low_X.append(y_axis_low[i] * x)
        i = i + 1 

    # data = []

    # data.append(
    #     go.Scatter(
    #         x = x_axis,
    #         y = y_axis_top,
    #     )
    # )
    # data.append(
    #     go.Scatter(
    #         x = x_axis,
    #         y = y_axis_low,
    #     )
    # )

    # fig = go.Figure(data = data)

    # plotly.offline.plot(fig, filename='test.html')

    i = 1
    stopR = 0
    stopL = 0
    min = 1
    min2 = 1
    while ( stopR != 1 or stopL != 1) :
        if stopL == 0 :
            if abs( ( sum( y_axis_low_X[0:i])/sum( y_axis_low[0:i]) ) - ( sum( y_axis_top_X[i:202])/sum( y_axis_top[i:202]) ) ) < min :
                yl = x_axis[i]
                min = abs( ( sum( y_axis_low_X[0:i])/sum( y_axis_low[0:i]) ) - ( sum( y_axis_top_X[i:202])/sum( y_axis_top[i:202]) ) ) 
        if stopR == 0 :
            if abs( ( sum( y_axis_top_X[0:i])/sum( y_axis_top[0:i]) ) - ( sum( y_axis_low_X[i:202])/sum( y_axis_low[i:202]) ) ) < min2 :
                yr = x_axis[i]
                min2 = abs( ( sum( y_axis_top_X[0:i])/sum( y_axis_top[0:i]) ) - ( sum( y_axis_low_X[i:202])/sum( y_axis_low[i:202]) ) ) 
        i = i + 1
        if( i == 201 ) :
            break
    # print('OMG')
    # print( min,min2 )
    # print(yl, yr)
    # print( (yl+ yr)/2 )
    return yl, yr


def outputEachRule (result_top, result_low, result_rule, output_feature_top, output_feature_low, n_class) :
    # print('OUTPUT EACH RULES')
    outputs = []
    for i in range(0, n_class) :
        outputs.append( [] )
    # print(outputs)
    # x_axis = np.linspace(0,3,501)
    for i in range(0,len(result_top)) :
        for j in range(0, n_class ) :
            if j == result_rule[i] :
                # outputs[result_rule[i]].append( [ result_top[i], result_low[i], 1 ] )
                # centroid()
                yl, yr = centroid(result_top[i], result_low[i], 1, output_feature_top, output_feature_low)
                outputs[result_rule[i]].append( [ result_top[i], result_low[i], yl, yr , 2 ] )
            else : 
                yl, yr = centroid(result_top[i], result_low[i], 0, output_feature_top, output_feature_low)
                # outputs[j].append( [ result_top[i], result_low[i], 0 ] )
                outputs[j].append( [ result_top[i], result_low[i],yl, yr, 1 ] )
            # break
    # for output in outputs :
    #     print(output)
    return outputs



def summaryOutput ( output_feature_top, output_feature_low, outputs ) :
    x_axis = np.linspace(0,3,501)
    y_axis = []
    result = []
    for i in range(0, len(outputs)) :
        y_axis.append( [ [], [] ] )
        result.append( [] )
    i = 0
    for output in outputs :
        yes = output[0]
        no = output[1]
        for x in x_axis :
            y_temp_top_yes = 0
            y_temp_top_no = 0
            y_temp_low_yes = 0
            y_temp_low_yes = 0

            y_temp_top_yes = triangle(output_feature_top[1] , x)
            if y_temp_top_yes > yes[0] :
                y_temp_top_yes = yes[0]

            y_temp_top_no = triangle(output_feature_top[0] , x)
            if y_temp_top_no > no[0] :
                y_temp_top_no = no[0]            

            y_temp_low_yes = triangle(output_feature_low[1] , x)
            if y_temp_low_yes > yes[1] :
                y_temp_low_yes = yes[1]

            y_temp_low_no = triangle(output_feature_low[0] , x)
            if y_temp_low_no > no[1] :
                y_temp_low_no = no[1]

            y_axis[i][0].append(np.max([ y_temp_top_yes , y_temp_top_no]))
            y_axis[i][1].append(np.max([ y_temp_low_yes , y_temp_low_no]))
        i = i + 1 
    return x_axis, y_axis, result


def defuzzy( outputs ) :
    result = []
    # print('DEFUZZ')
    for output in outputs :
        # print('==========')
        # print('OUTPUT')
        # for x in output :
        #     print(' ' + str(x))
        outputSortedYL = output
        outputSortedYR = output
        outputSortedYL = sorted(outputSortedYL, key=itemgetter(2))
        outputSortedYR = sorted(outputSortedYR, key=itemgetter(3))
        # print('sorted by yl')
        # print(outputSortedYL)
        # for x in outputSortedYL :
        #     print(' ' + str(x) + '--> yl = ' + str(x[2]))
        # print('sorted by yr')
        # print(outputSortedYR)
        # for x in outputSortedYR :
        #     print(' ' + str(x) + '--> yr = ' + str(x[3]))
        #YR
        # print('CALCULATE YR')
        yr = 0
        fr = initFR(outputSortedYR)
        # print('INIT FR')
        # print(fr)
        # print('CAL INIT YR')
        for i in range(0,len(fr)) :
            yr = yr + (fr[i] * outputSortedYR[i][3])
        #     print('  yr = ' + str(yr))
        # print('  sum(fr) = ' + str(sum(fr)))    
        yr = yr /  ( sum(fr) + 0.00000000001 )
        # print('INIT YR')
        # print(yr)
        yrI = yr
        for i in range(0,len(outputSortedYR)) :
            # print('R' + str(i))
            fr = FRforYR(outputSortedYR, i)
            # print(' FR when' + 'R' + str(i))
            # print(' ' + str(fr))
            yr = 0
            # print('\tCalculate')
            for j in range(0,len(fr)) :
                yr = yr + (fr[j] * outputSortedYR[j][3])
                # print('\t' + str(fr[j]) + '*' + str(outputSortedYR[j][3]) + '-->' + str(yr))
            # print('\t' + str(yr))
            # print('\tsum fr ' + str(sum(fr)))
            yr = yr / sum(fr)
            # print('\t' + str(yr))
            yrII = yr
            if yrII == yrI :
                yr = yrII
                # print('HINT!!!! ' + str(i))
                break
            else :
                yrI = yrII
            # print(yr, yrI, yrII)
        #YL
        # print('CALCULATE YL')
        yl = 0
        fr = initFR(outputSortedYL)
        # print('INIT FR')
        # print(fr)
        # print('CAL INIT YL')
        for i in range(0,len(fr)) :
            yl = yl + (fr[i] * outputSortedYL[i][2])
        #     print('  yr = ' + str(yl))
        # print('  sum(fr) = ' + str(sum(fr)))    
        yl = yl / ( sum(fr) + 0.00000000001  )
        # print('INIT YR')
        # print(yl)
        ylI = yl
        for i in range(0,len(outputSortedYL)) :
            # print('R' + str(i))
            fr = FRforYL(outputSortedYL, i)
            # print(' FR when' + 'R' + str(i))
            # print(' ' + str(fr))
            yl = 0
            # print('\tCalculate')
            for j in range(0,len(fr)) :
                yl = yl + (fr[j] * outputSortedYL[j][2])
                # print('\t' + str(fr[j]) + '*' + str(outputSortedYL[j][3]) + '-->' + str(yl))
            # print('\t' + str(yl))
            # print('\tsum fr ' + str(sum(fr)))
            yl = yl / sum(fr)
            # print('\t' + str(yl))
            ylII = yl
            if ylII == ylI :
                yl = ylII
                # print('HINT!!!! ' + str(i))
                break
            else :
                ylI = ylII
            # print(yl, ylI, ylII)
        # print( '----------->' + str( yl) + ' ' +  str(yr) + ' ' + str((yr+yl)/2) )
        result.append( (yr+yl)/2 )
    # print(result)
    return result


def initFR ( output ) :
    fr = []
    for out in output :
        fr.append( ( (out[0]+out[1]) / 2 ) + 0.00000000001 )
    return fr

def FRforYR ( output, R) :
    fr = []
    i = 0
    for out in output :
        if i <= R :
            fr.append( out[1] )
        else : 
            fr.append( out[0] )
        i = i + 1
    return fr

def FRforYL ( output, L) :
    fr = []
    i = 0
    for out in output :
        if i <= L :
            fr.append( out[0] )
        else : 
            fr.append( out[1] )
        i = i + 1
    return fr