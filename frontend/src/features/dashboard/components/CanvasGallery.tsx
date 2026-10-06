import React, { useEffect, useState } from "react"
import { type StoredCanvas, type CanvasSubmission } from "../../../models/CanvasModels"
import axios from "axios"
import { useAuth } from "../../../components/AuthContext"
import "./CanvasGallery.css"
import DrillCard from "./DrillCard"
import { useNavigate } from "react-router-dom"

const CanvasGallery = () => {
    
    const [canvasList, setCanvasList] = useState<StoredCanvas[]>([])
    const [message, setMessage] = useState("")
    const [isLoading, setIsLoading] = useState(false)
    const {user, loading} = useAuth()
    const navigate = useNavigate()
    const loadCanvasList = () => {
        try {
            setMessage("Loading...")
            setIsLoading(true)
            axios
                .get("/api/v1/canvas-drawing/", {
                    withCredentials: true,
                    headers: {"Content-Type": "application/json"}
                })
                .then((resp) => {
                    const data: StoredCanvas[] = resp.data
                    setCanvasList(data)
                })
                .catch(() => {
                    console.log("An error occurred fetching ")
                })
        } catch {
            setMessage("An error has occurred fetching canvases. Try again later...")
        } finally {
            setIsLoading(false)
        }
    }
    const handleNewCanvas = (e: React.MouseEvent) => {
        e.preventDefault()
        if (!user) return
        const submission: CanvasSubmission = {
            name: "My First Drill",
            template: "full_hockey_rink",
            data: {lines: [], shapes: []},
            visibility: "private",
        }
        axios
            .post(
                "api/v1/canvas-drawing/",
                submission,
                {withCredentials: true, headers: {"Content-Type": "application/json"}}
            )
            .then((resp) => {
                const data: StoredCanvas = resp.data
                window.location.href = `/canvas-drawing/${data.id}`
                return
            })
            .catch(() => {console.log("An error occurred loading your data...")})
    }

    const onCardDelete = (drillId: string) => {
        axios
            .delete(
                `api/v1/canvas-drawing/${drillId}/`, 
                {withCredentials: true},
            )
            .then(() => setCanvasList(canvasList.filter((drill) => drill.id !== drillId)))
            .catch(() => console.error("An error occurred deleting drill:", drillId))
    }

    const onEdit = (drillId: string) => {
        navigate(`/canvas/${drillId}`)
    }

    useEffect(loadCanvasList, [])
    if (loading){
        return <h1>Loading...</h1>
    } else if (!user) {
        window.location.href = "/"
        return <h1>Log in!</h1>
    }
    return(
        <section className="canvas-gallery">
            <div className="gallery-header">
                <h1>My Drills Gallery</h1>
                {isLoading && <h1>{message}</h1>}
                <button className="gallery-btn" onClick={handleNewCanvas}>+ Create New Drill</button>
            </div>
            <div className="cards-grid">
                {canvasList.map(
                    (drill) => {
                        console.log(drill)
                        return <DrillCard
                            key={drill.id}
                            drill={drill}
                            onEdit={onEdit}
                            onDelete={onCardDelete}
                        />
                    }
                    )}
            </div>
        </section>
    )
}

export default CanvasGallery