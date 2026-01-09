# シェルスクリプトについて
コマンドラインをあらかじめ記述しておくファイルのこと。

次のようなメリットがある。
- 同じ処理を使いまわせる（再利用）
- 他の人にも配布できる
- コマンドを打ち間違えることによる作業ミスをなくす

基本的には、`Bash`シェルを前提にスクリプトを書いておくことが無難。  
（互換性が無くてエラーが起こる可能性もある、、、）

下のスクリプトは、[「新しいLinuxの教科書」](https://www.sbcr.jp/product/4815624316/)を参考に作成。

## 基本的な使い方（最小構成）
/bin配下のコマンド群のファイルサイズの上位6番目までを表示するスクリプトを作ってみる。

`du -h /usr/bin/* | sort -rn | head -n 6`

1. com_size.shファイルを作成
    ```bash
    #!/bin/bash
    du -h /usr/bin/* | sort -rn | head -n 6
    ```
    ※ シバンは絶対パスで指定しておく。（`bin/bash`はエラー）

2. 実行権限を付与する  

    `chmod +x com_size.sh`

3. 実行する

    `./com_size.sh`で実行できる。  
    相対パスで指定するのが無難。

    `source`やシェルの引数で実行することもできるが、↑を使っておけばいい。

## 日記自動化スクリプト

```bash
#!/bin/bash

echo "hogehoge"

# 日記データの保存ディレクトリ
directory="${HOME}/test/diary"

# 保存ディレクトリがなければ作成する
if [ ! -d "directory" ]; then
    mkdir "$directory"
fi

diaryfile="${directory}/$(date '+%Y-%m-%d').txt"

if [ ! -e "${diaryfile}" ]; then
    date '+%Y-%m-%d' > "$diaryfile"
fi

vim "${diaryfile}"
```

## 擬似treeスクリプト

```bash
#!/bin/bash

list_recursive ()
{
    local filepath=$1
    local indent=$2

    echo "${indent}${filepath##*/}"

    if [ -d "$filepath" ]; then
        # ディレクトリである場合は、
        # その中に含まれるファイルやディレクトリを一覧表示する
        local fname
        for fname in $(ls "$filepath")
        do
            # インデントにつベースを追加して再帰呼び出し
                list_recursive "${filepath}/${fname}" "    $indent"
        done
    fi
}

list_recursive "$1" ""
```

## findgrepスクリプト

```bash
#!/bin/bash

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
    directory='.'
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
```


# Tips

```bash
# エラーが起きたら終了する
set -e

hoge_env="test"
# -nで空文字ではないことを調べる
if [ -n "$1" ]; then
    hoge_env=$1
fi

# パッケージが入っているかチェック
# &> /dev/nullは標準出力、エラー出力を破棄するリダイレクト。結果は表示しない
dpkg -s python3-venv &> /dev/null

# -neはnot equal
if [ $? -ne 0 ]; then
    # -yは確認プロンプトをスキップして自動でyesにする
    apt-get -y install python3-venv
fi

# --system-site-packages: システム側のパッケージを継承してキャッシュを利用できる
python3 -m venv --system-site-packages eval_venv
source eval_venv/bin/activate

# pip自体のアップデート
pip install -U pip
pip install -r ./requirements.txt

# コンパイラに合わせたソースビルド
git clone -b v1.7.1 https://github.com/xxxyyyzzz.git
cd mmcv/
# 環境変数付きでパッケージをインストール
MAX_JOBS=8 MMCV_WITH_OPS=1 MMCV_WITH_CUDA=1 python setup.py install
cd ../ && rm -rf mmcv/

MAX_JOBS=4 pip install --no-build-isolation flash-attn==x.x.x
```