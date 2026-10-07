import GlobalHeader from "../../components/Header"
import CanvasGallery from "./components/CanvasGallery"

const DashboardPage = () => {
    return(
        <div>
            <GlobalHeader/>
            <main className="page-container">
                <CanvasGallery />
            </main>
        </div>
    )
}

export default DashboardPage