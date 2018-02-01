import numpy as np
from membership_test import firstMem, lastMem, triangle
import plotly
from plotly.graph_objs import Scatter, Layout
import plotly.graph_objs as go

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

def interface(out_low, out_top, rule_feature) :
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
        print('oooo')
        print(result_top[i])
        print(result_low[i])
        print(result_rule[i])
        print('yes')
        print(result_rule[i])
        print('no')
        for j in range(0, n_class):
            if j != result_rule[i] :
                print(j)
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
    print('------------')
    for x in out :
        print(x)
    return out

def summaryOutput ( output_feature_top, output_feature_low, outputs ) :
    x_axis = np.linspace(0,4,501)
    y_axis = []
    result = []
    for i in range(0, len(outputs)) :
        y_axis.append( [ [], [] ] )
        result.append( [] )
    i = 0
    for output in outputs :
        yes = output[0]
        no = output[1]
        print('-----')
        print(yes)
        print(no)
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

def defuzzy( output_feature_top, output_feature_low, outputs ) :
    x_axis, y_axis, result = summaryOutput( output_feature_top, output_feature_low, outputs )
    # print('Defuzz')
    for i in range(0, len(outputs)) :
        yr = Calyr_cen( x_axis, y_axis[i][1], y_axis[i][0])
        yl = yr
        yrI = yr
        ylI = yl
        ###yR
        for j in range(1, len(x_axis)-1 ) :
            if x_axis[j-1] >= yrI and yrI <= x_axis[j+1] :
                yrII = Calyr_yII(x_axis, y_axis[i][1], y_axis[i][0], j)
                if yrII == yrI or abs(yrII - yrI) < 0.001  :
                    yr = yrII
                    break
                else :
                    yrI = yrII
        ###yL
        for j in range(1, len(x_axis)-1 ) :
            if x_axis[j-1] >= ylI and ylI <= x_axis[j+1] :
                ylII = Calyl_yII(x_axis, y_axis[i][1], y_axis[i][0], j)
                if ylII == ylI or abs(ylII - ylI) < 0.001 :
                    yl = ylII
                    break
                else :
                    ylI = ylII
        result[i] = (yr+yl)/2

    print(result)
    plotResult( x_axis, y_axis, result )
    return result

def plotResult( x_axis, y_axis, result) :
    for i in range(0, len(result)) :
        x = x_axis
        y1 = y_axis[i][0]
        y2 = y_axis[i][1]
        trace1 = Scatter( x = x, y = y1 )
        trace2 = Scatter( x = x, y = y2 )
        trace3 = Scatter( x = [result[i], result[i]], y = [0, 1] )
        data = [ trace1, trace2, trace3 ]
        fig = go.Figure(data = data)

        plotly.offline.plot(fig, filename='output' + str(i) + '.html')

def Calyr_cen ( x_axis, y_axis_low, y_axis_top) :
    fr = []
    frMultiy = []
    for i in range(0, len(x_axis) ) :
        fr.append( (y_axis_low[i] + y_axis_top[i] ) / 2 )
        frMultiy.append( fr[i] * x_axis[i] )
    result = sum(frMultiy) / sum(fr)
    return result

def Calyr_yII ( x_axis, y_axis_low, y_axis_top, R ) :
    fr = []
    frMultiy = []
    for i in range(0, len(x_axis) ) :
        if i > R :
            fr.append( y_axis_top[i] )
        else :
            fr.append( y_axis_low[i] )
        frMultiy.append( fr[i] * x_axis[i] )
    result = sum(frMultiy) / sum(fr)
    return result

def Calyl_yII ( x_axis, y_axis_low, y_axis_top, L ) :
    fr = []
    frMultiy = []
    for i in range(0, len(x_axis) ) :
        if i <= L :
            fr.append( y_axis_top[i] )
        else :
            fr.append( y_axis_low[i] )
        frMultiy.append( fr[i] * x_axis[i] )
    result = sum(frMultiy) / sum(fr)
    return result