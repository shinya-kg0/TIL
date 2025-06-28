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
