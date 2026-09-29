import '../../App.css'
import {useState} from 'react'
import { useParams } from 'react-router-dom'
import Canvas from './components/Canvas'
import Palette from './components/Palette'

const CanvasEditorPage = ( {canvasId}: {canvasId: string}) => {
  const [activeTool, toolSetter] = useState("brush")
  // const { canvasId } = useParams();
  if ( !canvasId ){
    return <div>Error: No canvas ID specified...</div>
  }
  return (
    <>
      <PageHeader />
      <Palette activeTool={activeTool} toolSetter={toolSetter}/> 
      <section>
      <Canvas tool={activeTool} canvasId={canvasId}/>
      </section>
    </>
  )
}

const PageHeader = () => {
  return (
  <div><h1>Coach Lab Canvas</h1></div>
  )
}
export default CanvasEditorPage