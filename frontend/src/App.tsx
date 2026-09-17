import './App.css'
import {useState} from 'react'
import Canvas from './components/Canvas'
import Palette from './components/Palette'


const App = () => {

  const [activeTool, toolSetter] = useState("brush")
  return (
    <>
      <PageHeader />
      <Palette activeTool={activeTool} toolSetter={toolSetter}/> 
      <section>
      <Canvas tool={activeTool} />
      </section>
    </>
  )
}

const PageHeader = () => {
  return (
  <div><h1>Coach Lab Canvas</h1></div>
  )
}
export default App
