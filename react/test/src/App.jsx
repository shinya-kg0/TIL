import './App.css'
import Button from './components/Button/Button'
import Display from "./components/Display/Display"
import { useState, useEffect } from 'react';

function App() {

  const [count, setCount] = useState(0);

  const handleClick = () => {
    setCount(count + 1)
  }

  useEffect(()=>{
    console.log("count: ", count)
    if (count > 10) {
      setCount(0)
    }
  }, [count])

  return (
    // Reactは複数タグを書く時、全体を一つのタグで囲んでおかないとエラーになる
    <>
      <h1>Hello World!</h1>
      <Button type="submit" disabled={false} onClick={handleClick}>
        ボタン
      </Button>
      <div>
        <Display count={count}/>
      </div>
      
    </>
  )
}

export default App
