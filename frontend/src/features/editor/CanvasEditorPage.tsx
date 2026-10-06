import "./CanvasEditorPage.css"
import { useParams } from 'react-router-dom'
import CanvasEditor from './components/CanvasEditor'
import NavBar from '../../components/NavBar';
import GlobalHeader from '../../components/Header';

const CanvasEditorPage = () => {
  const { canvasId } = useParams();
  if ( !canvasId ){
    return <div>Error: No canvas ID specified...</div>
  }
  return (
    <main className="editor">
      <GlobalHeader />
      <PageHeader />
      <NavBar />
      <CanvasEditor canvasId={canvasId}/>
    </main>
  )
}

const PageHeader = () => {
  return (
  <div className="editor__section-header"><h2>Coach Lab Canvas</h2></div>
  )
}
export default CanvasEditorPage