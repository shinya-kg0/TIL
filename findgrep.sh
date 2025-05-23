#!/bin/zsh

pattern=$1
directory=$2
name=$3

usage ()
{
    # シェルスクリプトのファイル名を取得
    local script_name=$(basename "$0")

    # ヒアドキュメントでヘルプを表示
    cat << END
Usage: $script_name PATTERN [PATH] [NAME_PATTERN]
Find current directory recursively, and print lines which match PATTERN.

    PATH            find file in PATH directory, instead of current directory 
    NAME_PATTERN    specify name pattern to find file

Example:
    $script_name return 
    $script_name return ~ '*.txt'
END
}


# コマンドライン引数が0のとき
if [ "$#" -eq 0 ]; then
    usage
    exit 1      # ステータス1で終了
fi

# 第二引数が空文字なら、デフォルトでカレントディレクトリを指定
if [ -z "$directory" ]; then
    directory="./"
fi

# 第三引数が空文字ならデフォルトで'*'を指定する
if [ -z "$name" ]; then
    name='*'
fi

# 検索ディレクトリが存在しない場合はエラーメッセージを表示して終了
if [ ! -d "$directory" ]; then
    echo "$0: ${directory}: No such directory" 1>&2
    exit 2
fi

# -n: 行数の表示
# -H: 引数にファイルが一つだけでもマッチした行の前にファイル名を表示する
find "$directory" -type f -name "$name" | xargs grep -nH "$pattern"

# 使い方
# ./findgrep "基本" ./ "*how*"
# ./findgrep <検索したい文字列パターン> ./ <調べたいファイルのパターン> 
