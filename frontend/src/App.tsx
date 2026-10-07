import './App.css'
import { BrowserRouter, Routes, Route} from 'react-router-dom';
import CanvasEditorPage from './features/editor/CanvasEditorPage';
import LoginPage from './features/login/LoginPage';
import RegistrationForm from './features/register/RegisterPage';
import DashboardPage from './features/dashboard/DashboardPage';
import { AuthProvider } from './components/AuthContext';


const App = () => {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
            <Route path="/" element={<LoginPage/>}/>
            <Route path="/register" element={<RegistrationForm/>}/>
            <Route path="/dashboard" element={<DashboardPage/>}/>
            <Route path="/canvas/:canvasId" element={<CanvasEditorPage />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
    )
}

export default App