# 非同期処理まとめ

参考

- [非同期処理をシンプルなPythonコードで説明する](https://qiita.com/y_kato_eng/items/ca0de5cf1224c807e7e5)
- [Pythonの応用文法【非同期処理：async / await】](https://zenn.dev/umi_mori/books/python-programming/viewer/python-advanced-async-await)

- 非同期処理とは、、、
  - 一つのタスクが完了するのを待たずに、次のタスクに進むことができる処理


## 非同期処理の書き方

1. 非同期関数の定義
2. await式の使用
3. イベントループの実行（`asyncio.run()`）

```py
import asyncio

async def task1(name):
    print(f"{name}さん、こんにちは")
    await asyncio.sleep(1)
    print("こんにちは")
    return name

async def task2(name):
    print(f"{name}さん、こんばんは")
    await asyncio.sleep(2)
    print("こんばんは")
    return name

async def main():
    results = await asyncio.gather(
        task1("山田"),
        task2("鈴木")
    )
    print(results)

asyncio.run(main())
```


```py
import datetime
import aiohttp
import asyncio

start = datetime.datetime.now()

def log(message):
    print(f'{(datetime.datetime.now() - start).seconds}秒経過', message)

async def fetch(session, url):
    """非同期にURLからデータを取得する関数"""
    print(f"Fetching {url}")
    async with session.get(url) as response:
        return await response.text()

async def main():
    log("タスク開始")
    """メインの非同期処理を行う関数"""
    urls = [
        "http://google.com",
        "http://qiita.com",
        "https://www.python.org/",
        "https://www.mozilla.org/en-US/",
        "https://html.spec.whatwg.org/multipage/",
        "https://www.w3.org/TR/css/",
        "https://ecma-international.org/",
        "https://www.typescriptlang.org/",
        "https://www.oracle.com/jp/java/technologies/",
        "https://www.ruby-lang.org/ja/",
        "https://www.postgresql.org/",
        "https://www.mysql.com/jp/",
        "https://docs.djangoproject.com/ja/5.0/",
        "https://spring.pleiades.io/projects/spring-boot",
        "https://rubyonrails.org/"
        "https://firebase.google.com/?hl=ja",
        "https://go.dev/",
        "https://nodejs.org/en"
    ]
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        
        print("Starting tasks...")
        # 非同期タスクを開始する前にメッセージを出力
        print("Tasks are running in the background...")
        
        # 非同期タスクの結果を待つ
        results = await asyncio.gather(*tasks)
        
        print("Tasks completed. Results:")
        for result in results:
            print(result[:100])  # 結果の最初の100文字を表示
    
    log("タスク終了")

# asyncio.run()を使ってメイン関数を実行する
if __name__ == "__main__":
    asyncio.run(main())
```