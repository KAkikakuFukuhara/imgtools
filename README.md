# README

pythonを用いた画像処理用のプログラム群をまとめたプロジェクト.

![python](https://img.shields.io/badge/python-3.8%7C3.9%7C3.10-brightgreen)
![opencv](https://img.shields.io/badge/opencv-4.7.0.72-blue)

## 環境構築

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
cp scripts/imgtools.sh $HOME/.local/bin
vim $HOME/.local/bin/imgtools.sh # edit scripts file
```

```diff
- PROJ_DIR="." # repository abs path
+ PROJ_DIR=$HOME/imgtools # Example:imgtools abs path
```

## 使用方法

使用方法はサブコマンドを使用して実行したいプログラムを指定して実行する.
サブコマンドの一覧は以下のように`help`引数を渡して取得する。

```bash
imgtools.sh --help
```

サブコマンド移行の引数を知りたい場合は以下のようにサブコマンドを指定した後に`help`引数を渡す

```bash
imgtools.sh png2jpg --help
```




