import axios from "axios"
import type React from "react"

const NavBar = () => {
    const handleLogoutClick = (e: React.MouseEvent) => {
        axios
            .post("/api/login/logout")
            .then((resp) => {
                console.log("Logging out...")
            })
            .catch((resp) => {
                console.log("An unknown error has occurred")
            })
    }

    return(
        <div>
            <a href="/dashboard">Home</a>
            <a href="/profile">Profile</a>
            <a href="/" onClick={handleLogoutClick}>Logout</a>
        </div>
    )
}

export default NavBar