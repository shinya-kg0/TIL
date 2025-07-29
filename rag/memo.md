## インデクサーについて

役割：ドキュメントをベクトル化してDBなどに保存する

→ 今回はPDFから文字列を取得しチャンクに分解

→ ベクトルに埋め込んでAI Searchにインデックスとして登録する

別の方法としては、

- 階層的インデクシング
→ 詳細情報、複数のチャンクにまたがる統合情報の両方に対応
　 生のドキュメントと、異なる抽象化レベルの要約を一緒にインデックス化
　 どの抽象度の質問でも対応できるよ！
- 多表現インデクシング
→ 生ドキュメントと検索に使う単位を分離する
　 ドキュメントを要約したものを保存する。検索には要約ドキュメントを使い
　 その要約に関連する元ドキュメントを取得する
　 検索の効率○、生ドキュメントを活かせる！
- ColBERT
→ チャンクをより細かく保存しておいてクエリも分解して細かく比較
　 ドキュメントも単語やフレーズに分解、それぞれでベクトルを作成
　 質問も細かい単語レベルに分解、個別に対照し類似度を決める
　 より精密なマッチングが可能に！
- RAPTORは、階層的・構造化された長文データや複雑な文書体系に強み。
- Multi-Representation Indexingは、多粒度・多視点での検索が求められるFAQや教育、ニュースなどで効果的。
- ColBERTは、きめ細かい意味的マッチングが必要な大規模検索や専門分野、短文データに特に適しています


## AI Searchのパラメータ

リソースを作成

インデックスの作成が必要

1. algorithms（アルゴリズム）セクション

主に「HNSW（Hierarchical Navigable Small World）」か「Exhaustive KNN（K-Nearest Neighbor）」を指定し、詳細なパラメータを選択します。

| **パラメータ** | **説明** | **例・値** |
| --- | --- | --- |
| **`kind`** | アルゴリズムの種類を指定。**`hnsw`** または **`exhaustiveKnn`** | **`"kind": "hnsw"`** |
| **`metric`** | 類似度計算手法。**`cosine`**, **`dotProduct`**, **`euclidean`**, **`hamming`** | **`"metric": "cosine"`** |
| **`m`** | HNSWの双方向リンク数（グラフの複雑さ） | 4～10（デフォルト：4） |
| **`efConstruction`** | インデックス作成時の近傍数。検索精度と構築時間のトレードオフを調整 | 100～1000（デフォルト：400） |
| **`efSearch`** | 検索時の近傍数。リコール精度と検索速度の調整 | 100～1000（デフォルト：500） |
| **`exhaustiveKnnParameters.metric`** | Exhaustive KNN用の距離計算メトリック（例：**`euclidean`**） | **`"metric": "euclidean"`** |

2. compressions（圧縮）セクション

インデックス内のベクトル圧縮と、再ランクやオーバーサンプリングなど補助機能を設定できます

| **パラメータ** | **説明** | **例・値** |
| --- | --- | --- |
| **`kind`** | 圧縮種類。**`scalarQuantization`** または **`binaryQuantization`** | **`"kind": "scalarQuantization"`** |
| **`scalarQuantizationParameters.quantizedDataType`** | スカラー量子化時のデータ型。現状は**`int8`**のみ | **`"int8"`** |
| **`rerankWithOriginalVectors`** | 元の生ベクトルによる再ランク実施。省略時は**`true`** | true/false |
| **`defaultOversampling`** | 上位k件抽出時のオーバーサンプリング倍率。検索精度調整 | 数値（例：10） |
| **`truncationDimension`** | ベクトル維持の次元数（次元削減時に指定）[2](https://qiita.com/nohanaga/items/e0dad274be662863ea6a) | 数値 |

3. profiles（プロファイル）セクション

アルゴリズム・圧縮方式・（ベクトライザ）を組み合わせたプロファイルを定義し、各ベクトルフィールドで参照します[3](https://learn.microsoft.com/en-us/python/api/azure-search-documents/azure.search.documents.indexes.models.vectorsearchprofile?view=azure-python)。

| **パラメータ** | **説明** | **例** |
| --- | --- | --- |
| **`name`** | プロファイル名。vectorフィールドで参照 | **`"vector-profile-1"`** |
| **`algorithm`** | 利用アルゴリズム名 | **`"hnsw-1"`** |
| **`compression`** | 利用圧縮名（任意） | **`"scalar-quant"`** |
| **`vectorizer`** | ベクトライザ名（任意） | **`"text-embedding-ada-002"`** |

4. ベクトルフィールドで使う主なパラメータ

| **パラメータ** | **説明** | **例・値** |
| --- | --- | --- |
| **`name`** | フィールド名 | **`"contentVector"`** |
| **`type`** | データ型 | **`"Collection(Edm.Single)"`** |
| **`searchable`** | ベクトル検索できるようにする | true |
| **`retrievable`** | ベクトル値を検索結果で返すか | true/false |
| **`dimensions`** | ベクトル次元数（モデルに準拠） | 1536など |
| **`vectorSearchProfile`** | 適用プロファイル名 | **`"vector-profile-1"`** |


## LlamaIndexのクラス

- `SearchClient`: 低レベルなAPIクライアント。Azure AI Search サービスとの直接的な通信を担当し、インデックスへのデータの読み書きや検索を実行します。

- `AzureAISearchVectorStore`: LlamaIndex と Azure AI Search の橋渡し役。LlamaIndex のノード構造を Azure AI Search のインデックススキーマにマッピングし、SearchClient を使ってLlamaIndexの要求をAzure AI Searchに伝えます。

- `VectorStoreIndex`: LlamaIndexのRAGインデックス管理の中心。与えられたノードをベクトル化し、vector_store を介して永続化（インデックス化）し、後で検索可能な状態にします。

### SearchClient

- **役割**: SearchClient は、Azure AI Search サービス自体と直接やり取りを行う窓口です。

```py
search_client = SearchClient(
    endpoint=st.SEARCH_SERVICE_ENDPOINT,
    index_name=st.SEARCH_SERVICE_INDEX_NAME,
    credential=AzureKeyCredential(st.SEARCH_SERVICE_API_KEY),
)
```

これは、特定の検索インデックスに対して、ドキュメントの追加、更新、削除、そして検索クエリの実行といった低レベルな操作を行うための「道具」を提供します。


### AzureAISearchVectorStore

- **役割**: AzureAISearchVectorStore は、LlamaIndex の抽象化されたベクトルストアインターフェースを、Azure AI Search サービスに具体的にマッピングする役割を担います。

```py
vector_store = AzureAISearchVectorStore(
    search_or_index_client=search_client,
    id_field_key=ID_FIELD_KEY,
    chunk_field_key=CHUNK_FIELD_KEY,
    embedding_field_key=EMBEDDING_FIELD_KEY,
    metadata_string_field_key=METADATA_STRING_FIELD_KEY,
    doc_id_field_key=DOC_ID_FIELD_KEY,
    dim=1536
)
```

これは、LlamaIndex が扱うノードデータ（テキストチャンクとその埋め込み、メタデータ）を、Azure AI Search のインデックススキーマに合わせてどのように保存・検索するかを定義します。search_client を内部で利用して、実際に Azure AI Search との通信を行います。


### VectorStoreIndex

- **役割**: VectorStoreIndex は、LlamaIndex の RAG システムの中核となるコンポーネントで、情報のインデックス化と検索の両方を管理します。

```py
index = VectorStoreIndex(
    nodes=nodes,
    vector_store=vector_store,
    show_progress=True,
)
```

与えられた nodes (テキストチャンク) を受け取り、それらを埋め込みモデルでベクトル化し、その結果を vector_store を通じて Azure AI Search にアップロードするという「インデックス作成」のプロセスをオーケストレーションします。また、後でクエリエンジンを作成する際には、この index を通じて検索も行われます。