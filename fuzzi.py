from pylab import *
import numpy as np
import matplotlib.pyplot as plt
import numpy as np

numOfFeature=4
n_rule=[3,2,3,3]
input_feature_top=[[0.3250,0.5631,1.8233,1],[0.5631,1.8233,2.6188,1],[1.8233,2.6188,4.0769,1]],[[0.3226,0.6028,0.8677,1],[0.6028,0.8677,1,1]],[[0,0.0164,0.3462,1],[0.0164,0.3462,0.7592,1],[0.3462,0.7592,0.8,1]],[[0,0.0010,0.0423,1],[0.0010,0.0423,0.0973,1],[0.0423,0.0973,0.1,1]]
input_feature_low=[[0.3546,0.5631,1.6666,0.8757],[1.2477,1.8233,2.1866,0.4567],[2.0877,2.6188,3.5922,0.6676]],[[0.4440,0.6028,0.7529,0.5668],[0.7529,0.8677,0.9250,0.4332]],[[0.0035,0.0164,0.2764,0.7882],[0.1103,0.3462,0.6416,0.7153],[0.5542,0.7592,0.7795,0.4965]],[[0.00015209,0.0010,0.0362,0.8520],[0.0132,0.0423,0.0811,0.7062],[0.0730,0.0973,0.0985,0.4419]]

rule_feature=[
    [0,0,0,1,0],
    [0,0,1,1,0],
    [0,0,2,1,0],
    [0,0,0,2,0],
    [0,0,1,2,0],
    [0,0,2,2,0],
    [0,1,0,1,0],
    [0,1,0,2,0],
    [0,1,1,0,1],
    [0,1,1,1,1],
    [0,1,1,2,1],
    [0,1,2,0,1],
    [0,1,2,1,1],
    [0,1,2,2,1],
    [0,0,0,0,2],
    [0,0,1,0,2],
    [0,0,2,0,2],
    [0,1,0,0,2],
    [1,0,0,0,3],
    [1,0,1,0,3],
    [1,0,2,0,3],
    [1,1,0,0,3],
    [1,1,1,0,3],
    [1,1,2,0,3],
    [2,0,0,0,3],
    [2,0,1,0,3],
    [2,0,2,0,3],
    [2,1,0,0,3],
    [2,1,1,0,3],
    [2,1,2,0,3],
    [1,0,0,1,4],
    [1,0,1,1,4],
    [1,0,2,1,4],
    [1,1,0,1,4],
    [1,1,1,1,4],
    [1,1,2,1,4],
    [1,0,0,2,4],
    [1,0,1,2,4],
    [1,0,2,2,4],
    [1,1,0,2,4],
    [1,1,1,2,4],
    [1,1,2,2,4],
    [2,0,0,1,4],
    [2,0,1,1,4],
    [2,0,2,1,4],
    [2,1,0,1,4],
    [2,1,1,1,4],
    [2,1,2,1,4],
    [2,0,0,2,4],
    [2,0,1,2,4],
    [2,0,2,2,4],
    [2,1,0,2,4],
    [2,1,1,2,4],
    [2,1,2,2,4]
    ]

def triangle(fuzzi,x): 
    b,m,d,h=fuzzi
    M=0
    if(x>=b and x<=m):
        M= ((0-h)/(b-m))*(x-b)
    if (x>m and x<=d ):
        M= h+(h/(m-d))*(x-m)
    return M

def firstMem(fuzzi,x):
    b,m,d,h=fuzzi
    M=0
    if(x>=b and x<=m):
        M=h
    if (x>m and x<=d ):
        M= h+(h/(m-d))*(x-m)
    return M

def lastMem(fuzzi,x):
    b,m,d,h=fuzzi
    M=0
    if(x>=b and x<=m):
        M= ((0-h)/(b-m))*(x-b)
    if (x>m and x<=d):
        M= h
    return M



### main
out_low=[[],[],[],[]]
out_top=[[],[],[],[]]
input_feature=[0.1,0.80,0.1,0.80]
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

result_top=[]
result_low=[]
result_rule=[]

i=0
while(i<len(rule_feature)):
    flag=True
    s_top=[]
    s_low=[]
    for j in range(0,size(rule_feature[i])-1):
        if(rule_feature[i][j]==-1):
            for kk in range(0,n_rule[j]):
                temp_rule=[]
                for k in range(0,size(rule_feature[i])):                    
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
        count=count+1       
        result_low.append(min(s_low))
        result_top.append(min(s_top))
        result_rule.append(rule_feature[i][len(rule_feature[3])-1])
    i+=1    

# print(rule_feature)
# print(len(rule_feature))
# print(count)

print(result_top)
print(result_low)
print(result_rule)

