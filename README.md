League of Legendsのクローラー
=======================

## 説明
 Leagure of Legendsをクロールするためのプログラム。
 APIを利用して取得を行う．
 ひとまずデータを取ってチームワークの研究に使えないか検討

## How to Use
- lolapi.py: LoLのAPIをまとめたライブラリ
- lolcrawler.py: LoLのCrawler本体
- inputMongoDB.py: 取得したデータをMongoDBに格納する
- crontabSample.txt: cronの設定例
- sampleAnalysis.py: 試しにMongoDB内のデータを集計してみた例

```
python lolCrawler.py
```

## クロールしたデータについて
- resultyyyymmddHH/gameIDxxxxxxx.json の形式で保存
- gameIDは同じものが時々複数あるので注意

## Files
- lolCraler.py: LoLのクローラー本体.

## Memos
- FeaturedGamesからGameIDとSummonerNameを取得→SummonerNameからSummonerID取得→SummonerID，GameIDから詳細データ取得
という流れが良さそう


## クロールの流れ
1. FeaturedGamesで最近のゲームを取得
2. ParticipantsのSummonerNamesを取得
3. SummonerNamesを使ってSummonerIdを取得
4. SummonerIdを使ってSummonerGamesを取得
5. SummonerGamesからMatchStatsを取得
6. 保存

## tatooineのmongodbの入り方(コマンドライン)
1. mongo
2. use admin
3. db.auth("tang","ud0nud0n")
4. use lol
5. show dbs






