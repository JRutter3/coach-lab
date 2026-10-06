import axios from "axios"
import "./NavBar.css"

const NavBar = () => {
    const handleLogoutClick = () => {
        axios
            .post("/api/login/logout")
            .then(() => {
                console.log("Logging out...")
            })
            .catch(() => {
                console.log("An unknown error has occurred")
            })
    }

    return(
        <nav className="nav-bar">
            <a href="/dashboard">Home</a>
            <a href="/profile">Profile</a>
            <a href="/" onClick={handleLogoutClick}>Logout</a>
        </nav>
    )
}

export default NavBar