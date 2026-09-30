# imgtools

Python と OpenCV を使った、画像・動画処理用のコマンドラインツール集です。画像フォルダの一括リサイズや回転、画像からの動画作成などをサブコマンドで実行できます。

## 目次

- [1. 必要環境](#1-必要環境)
- [2. インストール](#2-インストール)
  - [2.1 `imgtools.sh` コマンドの作成（任意）](#21-imgtoolssh-コマンドの作成任意)
- [3. コマンド](#3-コマンド)
- [4. 使用例](#4-使用例)
- [5. ライセンス](#5-ライセンス)

## 1. 必要環境

- Python 3.8〜3.10
- 依存パッケージは `pyproject.toml` に記載（OpenCV、Pillow、Matplotlib、tqdm、python-magic）

## 2. インストール

```bash
git clone https://github.com/KAkikakuFukuhara/imgtools.git
cd imgtools
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

仮想環境を有効にした状態なら、リポジトリのルートから次のように実行できます。

```bash
python tools --help
```

### 2.1 `imgtools.sh` コマンドの作成（任意）

プロジェクト外からも `imgtools.sh` として呼び出したい場合は、次を実行します。

```bash
bash scripts/create_bashscripts.sh
```

スクリプトは `$HOME/.local/bin/imgtools.sh` を作成します。`$HOME/.local/bin` が `PATH` に含まれていない場合は追加してください（例：`export PATH="$HOME/.local/bin:$PATH"`）。作成したランチャーはプロジェクト内の `.venv/bin/python` を使うため、先に上記のインストールを済ませてください。

## 3. コマンド

コマンド一覧と各コマンドのオプションは `--help` で確認できます。

```bash
python tools --help
python tools resize --help
```

ランチャーを作成した場合は `python tools` の代わりに `imgtools.sh` を使えます。

| サブコマンド | 機能 |
| --- | --- |
| `makeMP4` | 画像フォルダから MP4 動画を作成 |
| `count_resolution` | 画像フォルダ内の解像度ごとの枚数を集計 |
| `resize` | 画像を一括リサイズ |
| `rotate` | 画像を一括回転 |
| `concat` | 2つの画像フォルダの画像を順番に連結 |
| `png2jpg` | PNG 画像を JPEG に変換 |
| `rgb2gray` | 画像をグレースケールに変換 |
| `imshow` | 2つの画像フォルダの画像を表示・比較 |
| `diff` | RGB チャンネルの差分を表示 |
| `mp4_to_gif` | MP4 動画を GIF に変換 |
| `get_frames` | MP4 動画からフレーム画像を抽出 |

## 4. 使用例

```bash
# 画像を 640×480 にリサイズ（確認入力を省略）
python tools resize ./images --resolution 640x480 --y

# 画像を右に90度回転
python tools rotate ./images --rotate r90 --y

# 画像フォルダから動画を作成（毎秒30フレーム）
python tools makeMP4 ./images --fps 30 --out_file ./out.mp4

# サブコマンド固有の引数を確認
python tools mp4_to_gif --help
```

多くの画像処理コマンドは `.jpg` / `.png` を対象とし、入力フォルダ直下のファイルを処理します。オプションや出力先の既定値はコマンドごとに異なるため、実行前に `--help` を確認してください。

## 5. ライセンス

詳細は [LICENSE.md](LICENSE.md) を参照してください。
