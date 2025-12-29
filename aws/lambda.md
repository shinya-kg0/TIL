# Lambda関数の書き方

S3へのファイルアップロードをトリガーにして、データを処理（例：テキストの全大文字化や簡単なフィルタリング）し、別のバケットへ保存するPythonコードの例を紹介します。

この構成は「データクレンジング」や「ファイル形式変換」の基本パターンです。

### 1. Lambda関数のコード例 (`lambda_function.py`)

このコードは、アップロードされたテキストファイルの中身を読み取り、すべて大文字に変換して出力バケットに保存する例です。

```python
import json
import urllib.parse
import boto3

# S3クライアントの初期化（ハンドラーの外で行うことで再利用）
s3 = boto3.client('s3')

def lambda_handler(event, context):
    # 1. イベントからバケット名とファイル名を取得
    # S3イベントの構造から情報を抽出します
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    # ファイル名にスペースなどがある場合、URLエンコードされているのでデコードする
    object_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    # 保存先のバケット名を指定（実際のご自身のバケット名に変更してください）
    destination_bucket = 'your-output-bucket-name'
    
    try:
        # 2. 元ファイルを読み込む
        response = s3.get_object(Bucket=source_bucket, Key=object_key)
        content = response['Body'].read().decode('utf-8')
        
        # 3. データの加工処理（例：テキストをすべて大文字にする）
        processed_content = content.upper()
        
        # 4. 加工後のデータを別のバケットに保存
        # 元のファイル名に 'processed-' という接頭辞をつけて保存
        new_key = f'processed-{object_key}'
        s3.put_object(
            Bucket=destination_bucket,
            Key=new_key,
            Body=processed_content,
            ContentType='text/plain'
        )
        
        print(f"Successfully processed {object_key} and saved to {destination_bucket}")
        
        return {
            'statusCode': 200,
            'body': json.dumps('Processing complete!')
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        raise e

```

---

### 2. 事前に必要な準備（ここが重要です）

コードを書くだけでは動きません。以下の設定をAWSコンソールで行う必要があります。

#### ① バケットの用意

* **入力用バケット**（例：`my-input-data-bucket`）
* **出力用バケット**（例：`your-output-bucket-name`）

#### ② IAMロール（権限）の設定

Lambda関数に割り当てる実行ロールに、以下の権限が必要です。

* `AmazonS3ReadOnlyAccess`（入力バケットから読み取るため）
* `AmazonS3FullAccess`（出力バケットへ書き込むため）
* ※本来は特定のバケットに絞るのがベストですが、学習時はこの権限でOKです。


* `AWSLambdaBasicExecutionRole`（CloudWatchにログを出すため）

#### ③ トリガーの設定

Lambdaのコンソール画面で「トリガーを追加」をクリックし、S3を選択します。

* **Bucket**: 入力用バケットを選択
* **Event type**: `All object create events`（作成・アップロード時）
* **Prefix/Suffix**: 必要に応じて（例：`.txt` ファイルのみ対象にする場合など）

---

### 3. テストの仕方

1. Lambdaコンソールで「Deploy」をクリックしてコードを保存します。
2. 入力用S3バケットに、何か適当な英語のテキストファイル（例：`test.txt`）をアップロードします。
3. 数秒後、出力用S3バケットに `processed-test.txt` ができているか確認します。
4. うまくいかない場合は、Lambdaの「Monitor」タブから **CloudWatch Logs** を見ると、エラー内容が確認できます。

