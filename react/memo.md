# CSSについて

## 命名はキャメルケースを使う！

ハイフンを使うと読み込む時にエラーが出る。

# ディレクトリ構成について

## コンポーネントはまとめる

基本的にcomponentsディレクトリを作ってその中にコンポーネントごとの.jsx, .cssなどをまとめておくとよい！

# Hooksについて

※ コンポーネントの頭文字は大文字で書く

## 状態管理の基本（useState）

count, setCountを一緒に定義する。

- countは値を表示させるような役割。
- setCountはhandleXxxなどで状態を変化させたい時に使う役割

基本的には親コンポーネントに定義して、propsで値を渡すことがよい（共有が簡単にできる）  
→ 上から下に流すことが大事！


## 複数のコンポーネント

別のコンポーネントにそれぞれpropsを渡して親コンポーネントが共有していれば、複数のコンポーネント間で管理できる

## useEffect

副作用のためのフック

副作用とは・・・プログラムが本来の目的以外のことをする場合に使いたい処理  
例えば、Xの通知を押すと、そのページに遷移することが目的だが、通知アイコンのバッチを消すことも必要

### 使い方

関数の中かつreturnの前に定義しておく

引数を2つ持つ！  
第一引数にコールバック関数  
第二引数に配列を指定

例えば、countの値が変更になった時だけここに書いた関数が実行される

```js
  useEffect(()=>{
    console.log("count: ", count)
    if (count > 10) {
      setCount(0)
    }
  }, [count])
```

もし配列を空にすると、コンポーネントが画面に初回表示された時だけ実行されるようになる。

# ルーティングについて

ルーティングの基本構成

```js
import './App.css'
import { BrowserRouter, Routes, Route } from 'react-router-dom'

import Home from './pages/Home'
import SamplePage from './pages/SamplePage'

function App() {

  return (

    <>
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<Home />}/>
        <Route path='/sample-page' element={<SamplePage/ >} />
      </Routes>
    </BrowserRouter>
    </>
  )
}

export default App
```


Linkを使ってルーティングを設定できる！

```js
import { Link } from "react-router-dom"

function Home(){
    return (
        <>
            <h1>Home</h1>
            <Link to="/sample-page">Sample Pageへ！</Link>
        </>
    )
}

export default Home
```


# 拡張機能

- ブラウザdevツールでComponentsタブを使うことで確認がしやすい！
- VScodeの拡張機能で`rfc`というスニペットを使うことで、コンポーネントの基本構造のショトカができる！

# クイズゲームを作ってみる！

## 全体像を確認する

【ページ一覧】
1. TOPページ
2. クイズページ
3. 結果ページ

【機能一覧】
1. TOPページ
   - ボタン：押したらクイズページへ遷移
2. クイズページ
   - 問題文を表示
   - 選択肢を表示
   - 押したら、、、
        1. 正誤判定を行い、記録しておく  
        2-1. 問題文があれば次の問題を表示  
        2-2. 問題文がなければ結果ページへ遷移
3. 結果ページ
    - 表示までの演出（カーテンコール）を2秒表示させて非表示
    - クラッカー演出
    - 問題総数と正解数を取得し、表示