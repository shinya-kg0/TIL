# 環境構築

はじめは、対象のディレクトリを作って`npm create vite@latest`を実行Project nameを`.`にして展開する。


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

## ページコンポーネントを作成

まずは各コンポーネントの土台を作って、ルーティングを行う

各コンポーネントで`rfc`を用意しておく

## ルーティングの設定

`npm install react-router-dom`でルーティングに必要なパッケージをインストール

定数を別ファイルにまとめておく
```js
export const ROUTES = {
    HOME: "/",
    QUIZ: "/quiz",
    RESULT: "/result"
}
```

※ 2単語以上はアンダースコアをつける（`ROUTE_PATH`）

App.jsxのreturn内にレンダリング用のコードを記載

```js
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path={ROUTES.HOME} element={HomePage}/>
          <Route path={ROUTES.QUIZ} element={QuizPage}/>
          <Route path={ROUTES.RESULT} element={ResultPage}/>
        </Routes>
      </BrowserRouter>
    </>
  )
```

## TOPページの作成

タイトルとQuizページにレンダリングする用のLinkコンポーネントを追加

クイズの内容は、別で用意しておく

## クイズページのコンポーネントを作成

まずは静的に表示させる。Display.jsxを追加

`XXX.module.css`はスペルミスに注意  
modulesにすると表示されない

まずは静的に作ってみて、そこから動的に動かしていく方針が良い

小さいコンポーネントは`children`でデータを渡して、cssで装飾したりする。  
一つ上のコンポーネントにデータを取得するロジックを書いて、子コンポーネントに渡す

### mapの使い方

その要素を一意に特定するために、`key`を設定しておく必要がある！

他にも色々な使い方ができる！https://zenn.dev/mhirata/articles/c78f34123587c7

```js
    return (
        <>
            <Display>
                {`Q1. ${quizData[quizIndex].question}`}
            </Display>
            {
                quizData[quizIndex].options.map((option, index) => {
                    return <Button key={`option-${index}`}>{option}</Button>
                })
            }
        </>
    )
```

※ cmd + Shift + Pでコマンドパレットを開き`Format Document`を使うことでインデントを綺麗に揃えることができる！

## クイズの正誤判定ロジック

定数にしていたものを`useState, useEffect`を使いながらロジックを実装していく

### 関数型更新

useStateは現在のstate変数を引数として受け取れる！
```js
// 初めの状態ではprevに初期値の0が入っている
setQuizIndex((prev) => prev + 1);

// これは推奨されない
// 仮に2回呼び出した時にまとめて処理されることもあるため、バグの原因に！
setQuizIndex(quizIndex + 1);
```

### スプレッド構文

より簡単に配列の要素を追加できる！
```js
// 現在のstate変数を引っ張ってきて、trueを追加する処理を書いている
setAnswerLogs((prev) => [...prev, true]);
```

## useEffectで全問回答後にページ遷移させる
answerLogsが更新されるたびにその問題を全て回答したかをチェックする

navigationは2つの引数を受け取ることができる
- 遷移したいパス
- 渡したい値

```js
    useEffect(() => {
        if(answerLogs.length === MAX_QUIZ_LEN) {
            navigation(ROUTES.RESULT, {
                state: {
                    maxQuizLen: MAX_QUIZ_LEN
                }
            });
        }
    }, [answerLogs])
```

### .filter()で正解数だけカウントする
条件式を使ってその条件にあうような新しい配列を作る

```js
  correctNum = answerLogs.filter((answer) => {
      return answer === true
  })
```

### 条件付きレンダリング

`&&`は条件文でAND条件を設定したい時に使う論理演算子

問題数を制御するなどに使える！

```js
// quizData[quizIndex]が存在するならDisplayをレンダリングする
  {quizData[quizIndex] && <Display>{`Q1. ${quizData[quizIndex].question}`}</Display>}


// if/elseのような書き方もできる！
  {quizData[quizIndex] ? <Display>{`Q1. ${quizData[quizIndex].question}`}</Display> : <p>エラーが発生</p>}
```


## ソースコードの省略

実際は引数が一つの場合は括弧を省略しても良い

```js
setAnswerLogs((prev) => [...prev, true]);

setAnswerLogs(prev => [...prev, true]);
```

filterで1行の処理でreturnを返す場合は、省略できる！

```js
        if (answerLogs.length === MAX_QUIZ_LEN) {
            const correctNum = answerLogs.filter((answer) => {
                return answer === true
            })}

// こっちの方がスマート
        if (answerLogs.length === MAX_QUIZ_LEN) {
            const correctNum = answerLogs.filter(answer => answer === true)}
```

## データの受け取り

`useNavigate`のstateで情報は渡せるが、受け取るには？？

→ `useLocation`を使う！

```js
export default function ResultPage() {
    const location = useLocation();
    const maxQuizLen = location.state.maxQuizLen;
    const correctNumLen = location.state.correctNumLen;

    return (
        <>
            <h1>Result</h1>
            <p>あなたの正解数は...</p>
            <p>{`全${maxQuizLen}問中、${correctNumLen}問正解でした！`}</p>
```