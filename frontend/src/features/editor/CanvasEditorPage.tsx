import '../../App.css'
import { useParams } from 'react-router-dom'
import CanvasEditor from './components/CanvasEditor'
import NavBar from '../../components/NavBar';

const CanvasEditorPage = () => {
  const { canvasId } = useParams();
  if ( !canvasId ){
    return <div>Error: No canvas ID specified...</div>
  }
  return (
    <>
      <PageHeader />
      <NavBar />
      <CanvasEditor canvasId={canvasId}/>
    </>
  )
}

const PageHeader = () => {
  return (
  <div><h1>Coach Lab Canvas</h1></div>
  )
}
export default CanvasEditorPage