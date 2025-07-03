import { useState } from 'react'
import './App.css'
import { LinkButton } from './components/Link'

export const App = () => {
  const title: string = "Hello World!"
  const [num, setNum] = useState(0)

  const handleClick = () => {
    setNum(prev => prev + 1)
  }

  return (
    <>
      <div className='App'>
        <h1>{title}</h1>
        <LinkButton link="/test" text="ボタン" />
        <p>これまで{num}回押しました</p>
        <button type='button' onClick={handleClick}>数が増えます</button>
      </div>
    </>
  )
}

export default App

