# news category learning 

[クローラー](https://github.com/naronA/news_crawler)で集めたニュースをトークナイズ・ベクトル化します。
自宅環境で動くようにしているので汎用的なプログラムではありません。

```
.
├── ncl              # ルート
│   ├── data        # 各種データ
│   │   ├── csv    # ニュース原稿csv
│   │   ├── vector # ベクトル化データ
│   │   └── token  # トークナイズデータ
│   ├── learning    # 深層学習モジュール
│   │   └── ...
│   ├── old         # 使われなくなったコード
│   │   └── ...
│   ├── settings.py # 設定ファイル
│   ├── utils.py    # utilモジュール
│   └── vectorize   # ベクトル化モジュール
│       └── ...
├── main.py     # メイン
├── README.md
└── requirements.txt

```

## 動作確認環境

- OS: Windows Subsystem for Linux (Ubuntu16.04)
- CPU: Intel Core i7-4890K 4.00 GHz 
- Memory: 32G Byte

## 自宅環境

- FTP server address/path : 172.16.27.200/Crawler/YahooNews
    - ここにニュースがないと動作しない

### ニュース原稿をtokenizeする
トークナイズはmecab + neologdによって形態素解析した後に名詞、形容詞、動詞のみを取り出してファイルに保存します。
この処理はいずれクローラーサーバーに統合される予定です。

``` bash
python main.py tokenrize
```

### word2vec/doc2vecを用いてニュース原稿をベクトル化する
上のトークナイズ結果を使用してWord2Vecでベクトル化します。

``` bash
python main.py vectorize word2vec make_model
```

### TFIDF+主成分でニュース原稿をベクトル化する
こちらもトークナイズの結果を使用してTFIDFでベクトル化します。
7万次元以上になるため主成分分析で次元を減らします。
上記のスペックでも数時間掛かるので注意してください。

``` bash
python main.py vectorize tfidf
```

### TFIDFの深層学習を実行する
TFIDFの場合はベクトルを作成したあとTensorFlowを使用して深層学習ができます。
全体の8割データを使用して学習し、残り2割の未知のデータを使用して精度を測ります。

``` bash
python main.py deeplearning
```
