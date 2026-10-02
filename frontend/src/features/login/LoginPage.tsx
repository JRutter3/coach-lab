import LoginForm from "./components/LoginForm";
import logo from "../../assets/CoachLabLogo.jpeg"
import "../../App.css"

const LoginPage = () => {
    return (
        <div className="login-base">
            <div className="splash-logo">
                <img src={logo} width="500"/>
                <h1><b>COACH</b>LAB</h1>
                <h2>Collaborative Multi-Sport Whiteboard</h2>
            </div>
            <LoginForm />
        </div>
    )
}

export default LoginPage