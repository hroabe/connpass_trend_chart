# connpass_trend_chart
Connpas(IT勉強会プラットフォーム)のトレンドワードの集計・可視化スクリプトです

説明は↓です。


https://speakerdeck.com/hirokiabe/xing-tai-su-jie-xi-demian-qiang-hui-falsetorendowadowodiao-betemita

## nagisa
形態素解析モジュール nagisa でConpassのトレンドを解析するスクリプトです

```
$ python3 connpass.py
$ python3 create_chart.py ./
$ python3 create_trend_chart.py ./
```

## mecab
形態素解析モジュール MeCab + mecab-ipadic-NEologd でConpassのトレンドを解析するスクリプトです

```
$ python3 connpass_mecab.py
$ python3 create_chart.py
$ python3 create_trend_chart.py ./
$ python3 create_trend_language_chart.py ./
```

デフォルトでは1年分を集計しますが、connpass.py, conpass_mecab.pyを
変更することで集計期間を変更することができます
