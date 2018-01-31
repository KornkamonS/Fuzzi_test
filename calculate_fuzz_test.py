import numpy as np
from membership_test import firstMem, lastMem, triangle

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