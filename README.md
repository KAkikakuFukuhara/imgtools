# README

pythonを用いた画像処理用のプログラム群をまとめたプロジェクト.

![python](https://img.shields.io/badge/python-3.8%7C3.9%7C3.10-brightgreen)
![opencv](https://img.shields.io/badge/opencv-4.7.0.72-blue)

- [1. 環境構築](#1-環境構築)
- [2. 使用方法](#2-使用方法)

## 1. 環境構築

- ライブラリ等のインストール

```bash
git clone https://github.com/KAkikakuFukuhara/imgtools.git
cd imgtools
python -m venv .venv
source .venv/bin/activate
# pip install -U pip
# pip install -U setuptools
pip install -e ./
```

- ディレクトリに依存せず使用できるようにする方法

```bash
# export PATH=PATH;$HOME/.local/bin
# mkdir $HOME/.local/bin -p
bash scripts/create_bashscripts.sh
```

## 2. 使用方法

使用方法はサブコマンドを使用して実行したいプログラムを指定して実行する.
サブコマンドの一覧は以下のように`help`引数を渡して取得する。

```bash
python tools --help
# ディレクトリに依存しない場合
imgtools.sh --help

>>> usage: tools [-h] {makeMP4,count_resolution,resize,rotate,concat,png2jpg} ...
>>> 
>>> 画像関連の編集等のプログラムのコマンドラインパーサー
>>> 
>>> positional arguments:
>>>   {makeMP4,count_resolution,resize,rotate,concat,png2jpg}
>>>    makeMP4              画像セットから動画を作成する
>>>     count_resolution    ディレクトリに含まれる画像の解像度を調べるプログラム
>>>     resize               画像群をまとめてリサイズする
>>>     rotate               画像群をまとめて回転する
>>>     concat               画像を合成する
>>>     png2jpg             png画像群をjpg画像群に変換するプログラム
>>> 
>>> optional arguments:
>>>   -h, --help            show this help message and exit
```

サブコマンド移行の引数を知りたい場合は以下のようにサブコマンドを指定した後に`help`引数を渡す

```bash
imgtools.sh png2jpg --help
```
