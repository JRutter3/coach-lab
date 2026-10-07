import LoginForm from "./components/LoginForm";
import logoImage from "../../assets/CoachLabLogo.jpeg"
import "./LoginPage.css"

const LoginPage = () => {
    return (
        <div className="login-wrapper">
            <div className="login-card">
                <div className="login-brand">
                    <img src={logoImage} />
                    <h1>COACH<span className="title-accent">LAB</span></h1>
                    <h2>Collaborative Multi-Sport Whiteboard</h2>
                </div>
                <LoginForm />
            </div>
        </div>
    )
}

export default LoginPage