import "./Header.css"
import NavBar from "./NavBar"
import logo from "../assets/CoachLabLogo.jpeg"

const GlobalHeader = () => {
    return (
        <header className="header">
            <div className="header-container">
                <div className="brand">
                    <img src={logo} className="brand-logo"/>
                    <h1>COACH<span className="title-accent">LAB</span></h1>
                </div>
                <div className="nav-links">
                <NavBar />
                </div>
            </div>
            <hr />
        </header>
    )
}

export default GlobalHeader