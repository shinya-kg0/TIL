import './App.css'
import Button from './Button'

function App() {

  const handleClick = () => {
    console.log("button clicked")
  }

  return (
    // Reactは複数タグを書く時、全体を一つのタグで囲んでおかないとエラーになる
    <>
      <h1>Hello World!</h1>
      <Button type="submit" disabled={false} onClick={handleClick}>
        <span>クリック</span>
      </Button>
    </>
  )
}

export default App
