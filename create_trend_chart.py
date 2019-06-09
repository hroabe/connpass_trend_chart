import plotly
import plotly.graph_objs as go
import pandas as pd
import sys
from pathlib import Path
import os

def create_graphdata(path,graph_data_map,keywords):
    """
    グラフ用データを作成
    """
    p = Path(path)
    file_list = list(p.glob("*.csv"))
    file_list.sort()
    print(file_list)

    xaxis = []

    for fname in file_list:
        print("loading ..."  + str(os.path.basename(path)) )
        # CSVロード
        df = pd.read_csv(fname, engine="python",encoding="utf-8")
        df.columns = ['Keyword','Times']
        
        title = str(fname)
        xaxis.append(title[0:4] + '-' + title[4:6])

        for key in keywords:
            if not key in graph_data_map:
                    graph_data_map[key] = []            

            tmp = df[df['Keyword'] == key]
            
            if not tmp.empty:                
                graph_data_map[key].append(int(tmp['Times']))
            else:
                graph_data_map[key].append(0)

    return xaxis

if len(sys.argv) < 0:
    print("Please Specify CSV directory")
    exit(0)

path = str(sys.argv[1])
if path.endswith("/"):
    path += "/"

graph_list = []
graph_data_map = {}
keywords = [ 'AI','機械','統計','Python','Ruby','Java','AR','IoT','ブロック','Android','Unity']

xaxis = create_graphdata(path,graph_data_map,keywords)
print(graph_data_map)
print(xaxis)

num_of_stduy_group = pd.read_csv('num_of_study_group.csv', engine="python",encoding="utf-8")
num_of_stduy_group.columns = ['Date','Times']
data = go.Scatter(
    x=xaxis,
    y=num_of_stduy_group['Times']
)
graph_list.append(data)

for key in graph_data_map.keys():

    d = graph_data_map[key] 
    data = go.Scatter(
        x=xaxis,
        y=d
    )
    graph_list.append(data)

keywords.insert(0,'勉強会総数')
fig = plotly.tools.make_subplots(rows=3, cols=4, 
                                 subplot_titles=keywords)
fig.layout.height = 1200
fig.layout.showlegend=False

for idx,df in enumerate(graph_list):
    row = idx // 4 + 1

    fig.append_trace(df, row, (idx%4)+1)    

# グラフの作成
plotly.offline.plot(fig, filename='trend.html',auto_open=True)

print("Finish!")