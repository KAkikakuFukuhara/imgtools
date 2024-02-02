#!/bin/bash

# ディレクトリの作成
TARGETDIR=$HOME/.local/bin
mkdir $TARGETDIR -p && \
    echo "ディレクトリ作成：$TARGETDIR"

# 実行ファイルの作成
FILENAME="imgtools.sh"
FILEPATH=$TARGETDIR/$FILENAME
PROJDIR=$(cd $(dirname $0);cd ../;pwd)
echo "#!/bin/bash" > $FILEPATH && \
    echo "PROJDIR=$PROJDIR" >> $FILEPATH && \
    echo "\$PROJDIR/.venv/bin/python \$PROJDIR/tools \${@}" >> $FILEPATH && \
    echo "以下の実行ファイルを作成しました。" && \
    echo "$FILEPATH" && \
    echo "以下を実行して確認してください。" && \
    echo "$FILENAME --help"

# パーミッションの変更
chmod 775 $FILEPATH