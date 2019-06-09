import requests
import datetime
import nagisa
import time
import collections
import csv

url    = 'https://connpass.com/api/v1/event/'

# 過去1年を集計の対象にする
num_of_week = 12
target = []

now = datetime.datetime.today()
yd  = now.year
md  = now.month

for idx in range(num_of_week):
    md -= 1
    if md <= 0:
        md = 12
        yd = yd - 1    
    target.append([yd,md])

target.reverse()

text = {}

num_of_study_group = {}

for t in target:

    year  = str(t[0])

    # 10未満なら0を付ける
    if t[1] < 10:
        month = '0' + str(t[1])
    else:
        month = str(t[1])
    
    print(str(year) + '-' + str(month))
    
    # 総数を調べる
    param = 'ym=' + str(year) + month + '&count=100'    
    response     = requests.get(url + '?' + param)
    downloadData = response.json()

    count    = int(downloadData['results_available'])
    print("num of study group: " + str(count))

    num_of_study_group[year + month] = count

    # 取得回数
    loop = count // 100
    if count % 100 != 0 :
        loop += 1

    text[year + month] = []

    for idx in range(loop):
        param = 'ym=' + str(year) + month + '&start=' + str(100*idx) + '&count=100'
        response     = requests.get(url + '?' + param)
        downloadData = response.json()
       
        events = downloadData['events']
      
        for each_event in events:

            words = nagisa.extract(each_event['title'], extract_postags=['名詞'])
            text[year + month].extend(words.words)

            #words = nagisa.extract(each_event['description'], extract_postags=['名詞'])
            #text[year + month].append(words)
        
        time.sleep(3)

for key in text.keys():
    value = text[key]   
    result = collections.Counter(value)

    # 2文字以上の単語 かつ 出現回数が2回以上
    ranking = [ item for item in result.items() if len(item[0]) > 1 and item[1] > 1]
    # 降順にソート
    ranking = sorted(ranking, key=lambda x:x[1],reverse=True)

    print(key)
    print(ranking)

    # CSVファイルに保存する
    # conpass_keyword_yyyy-mm.csv
    with open(key + '.csv' , 'w') as f:
        writer = csv.writer(f)
        for word in ranking :
            writer.writerow(word)

with open('num_of_study_group.csv' , 'w') as f:
    for key in num_of_study_group.keys():
        f.write(key + ',' + str(num_of_study_group[key]) + '\n')    