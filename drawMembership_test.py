import numpy as np
import plotly
from plotly.graph_objs import Scatter, Layout
import plotly.graph_objs as go
from membership_test import getMF, triangle, firstMem, lastMem, getOutput
from rule_test import getRule

input_feature_top , input_feature_low, _, _ = getMF()
output_feature_top , output_feature_low = getOutput()
boundaries = [ 
    [0.325000000000000,	4.07692307692308],
    [0.322580645161290,	1],
    [0,	0.800000000000000],
    [0,	0.100000000000000],
    [0,0]
]


y_upper = []
x_upper = []
y_lower = []
x_lower = []

for feature in range(0,len(input_feature_top)) :
    y_upper.append([])
    x_upper.append([])
    y_lower.append([])
    x_lower.append([])
    # for graph in feature :
    for i in range(0,len(input_feature_top[feature])) :
        temp = [ 
            input_feature_top[feature][i][0], 
            input_feature_top[feature][i][1], 
            input_feature_top[feature][i][2]
        ]
        temp2 = [ 
            input_feature_low[feature][i][0], 
            input_feature_low[feature][i][1], 
            input_feature_low[feature][i][2]
        ]
        x_upper[feature].append(temp)
        x_lower[feature].append(temp2)
        hightest_low = input_feature_low[feature][i][3]
        if i == 0 :
            y_upper[feature].append([1, 1, 0])
            y_lower[feature].append([hightest_low, hightest_low, 0])
        elif i == len(input_feature_top[feature]) - 1 :
            y_upper[feature].append([0, 1, 1])
            y_lower[feature].append([0, hightest_low, hightest_low])
        else :
            y_upper[feature].append([0, 1, 0])
            y_lower[feature].append([0, hightest_low, 0])
        # y_upper[i].append([])
        # print(feature[i])
    # break

print(x_upper)
print(y_upper)

focus = 3
data = []
colors = ['orange', 'green', 'blue', 'pink']
for i in range(0,len(x_upper[focus])) :
    x = x_upper[focus][i]
    x2 = x_lower[focus][i]
    x_rev = x2[::-1]
    y1_upper = y_upper[focus][i]
    y1_lower = y_lower[focus][i]
    y1_lower = y1_lower[::-1]
    data.append(
        go.Scatter(
            x = x+x_rev,
            y = y1_upper+y1_lower,
            fill = 'tozerox',
            showlegend=False,
        )
    )

layout = go.Layout(
    xaxis=dict(
        range=[boundaries[focus][0],boundaries[focus][1]]
    ),
    height=400, 
    width=2000
)

fig = go.Figure(data = data, layout = layout)

plotly.offline.plot(fig, filename='test' + str(focus) + '.html')

# x = [0, 1, 2]
# x2 = [0.5000, 1.0000, 1.5000 ]
# x_rev = x2[::-1]
# y1_upper = [0, 1, 0]
# y1_lower = [0, 1, 0]
# y1_lower = y1_lower[::-1]
# trace1 = Scatter(
#             x = x+x_rev,
#             y = y1_upper+y1_lower,
#             fill = 'tozerox',
#             showlegend=False,
#         )
# x = [2, 3, 4]
# x2 = [2.5000, 3.0000, 3.5000]
# x_rev = x2[::-1]
# y1_upper = [0, 1, 0]
# y1_lower = [0, 1, 0]
# y1_lower = y1_lower[::-1]
# trace2 = Scatter(
#             x = x+x_rev,
#             y = y1_upper+y1_lower,
#             fill = 'tozerox',
#             showlegend=False,
#         )
# data2 = [ trace1, trace2 ]
# layout = go.Layout(
#     xaxis=dict(
#         range=[0, 4]
#     ),
# )

# fig = go.Figure(data = data2, layout = layout)

# plotly.offline.plot(fig, filename='output.html')