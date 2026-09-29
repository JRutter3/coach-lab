import './App.css'
import { BrowserRouter, Routes, Route} from 'react-router-dom';
// import CanvasEditorPage from './features/editor/CanvasEditorPage';
import LoginForm from './features/login/LoginPage';
import RegistrationForm from './features/register/RegisterPage';


const App = () => {
  return (
    <BrowserRouter>
      <Routes>
          <Route path="/" element={<LoginForm/>}/>
          <Route path="/register" element={<RegistrationForm/>}/>
          <Route path="/dashboard" element={<h1>Coming soon!</h1>}/>
      </Routes>
    </BrowserRouter>
  )
}

export default App

    {/*
    <BrowserRouter>
      <Routes>
          <Route path="/" element={<LoginForm/>}/>
          <Route path="/register" element={<RegistrationForm/>}/>
          <Route path="/dashboard" element={<h1>Coming soon!</h1>}/>
      </Routes>
    </BrowserRouter>
  */}
  