import plotly
import plotly.graph_objs as go
import pandas as pd
import sys
from pathlib import Path
import os

def create_graphdata(path,graph_data_map):
    """
    グラフ用データを作成
    """
    p = Path(path)
    file_list = list(p.glob("*.csv"))
    file_list.sort()
    print(file_list)

    for fname in file_list:
        if str(os.path.basename(fname))  == 'num_of_study_group.csv':
            continue

        print("loading ..."  + str(os.path.basename(path)) )
        # CSVロード
        df = pd.read_csv(fname, engine="python",encoding="utf-8")
        df.columns = ['Keyword','Times']

        title = str(fname)
        title = title[:title.rfind('.')]
        graph_data_map[title] = df       


if len(sys.argv) < 0:
    print("Please Specify CSV directory")
    exit(0)

path = str(sys.argv[1])
if path.endswith("/"):
    path += "/"

graph_list = []
graph_data_map = {}
create_graphdata(path,graph_data_map)

# グラフデータ
for idx,key in enumerate(graph_data_map):

    df = graph_data_map[key]
    df = df[0:20]
    data = go.Bar(
        x=df['Keyword'],
        y=df['Times'],
        opacity=0.7
    )
    graph_list.append(data)

graph_titles = list(graph_data_map.keys())
print(graph_titles)

fig = plotly.tools.make_subplots(rows=len(graph_titles)//4, cols=4, 
                                 subplot_titles=graph_titles)

fig.layout.height = 1000
fig.layout.showlegend=False

for idx,df in enumerate(graph_list):
    row = idx // 4 + 1
    
    fig.append_trace(df, row, (idx%4)+1)    

# グラフの作成
plotly.offline.plot(fig, filename='chart.html',auto_open=True)

print("Finish!")