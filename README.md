[![pages-build-deployment](https://github.com/FuJiK/YIELDCURVE3D/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/FuJiK/YIELDCURVE3D/actions/workflows/pages/pages-build-deployment)

# YIELDCURVE3D
US_YIELDCURVE3DModel

## 動作環境
Python3.9.9

## Files
- 3d_yield_curve_us.ipynb（Done）
- 3d_yield_curve_jp.ipynb(TBD 1.)
- getinvestingcom.ipynb(investpy APIがAPI仕様変更のため、うまく動作しない)
- getyieldcurvedata.ipynb (Python2系から３系へのリファクタ中)
- yieldcurvedata.py(取得したデータをgoogleスプレッドシートへ自動更新するためのPythonスクリプト、トークン取得のコードを書いてるのでTBD)

## TODO

1. 3d_yield_curve_jp.ipynbの日本銀行から取得する金利情報のスクレイピングのコードを追加
1. どこでも動くように、Docker-composeのリポジトリも準備
1. シェル書いてジョブ化（Databricks環境下では、ジョブ登録をDatabricks上でできるため不要）
1. getinvestingcom.ipynbのAPIエラー回避方法を模索