import GlobalHeader from "../../components/Header"
import NavBar from "../../components/NavBar"
import CanvasGallery from "./components/CanvasGallery"

const DashboardPage = () => {
    return(
        <div>
            <GlobalHeader/>
            <NavBar/>
            <h1>Canvas Gallery:</h1>
            <CanvasGallery />
        </div>
    )
}

export default DashboardPage