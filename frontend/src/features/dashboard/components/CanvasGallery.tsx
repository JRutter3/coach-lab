import React, { useEffect, useState } from "react"
import { type StoredCanvas, type CanvasSubmission } from "../../../models/CanvasModels"
import axios from "axios"
import { useAuth } from "../../../components/AuthContext"

const CanvasGallery = () => {
    
    const [canvasList, canvasListSetter] = useState<StoredCanvas[]>([])
    const [message, setMessage] = useState("")
    const [isLoading, setIsLoading] = useState(false)
    const {user, loading} = useAuth()
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
                    canvasListSetter(data)
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
            owner_id: user.id,
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

    useEffect(loadCanvasList, [])
    if (loading){
        return <h1>Loading...</h1>
    } else if (!user) {
        window.location.href = "/"
        return <h1>Log in!</h1>
    }
    return(
        <div className="canvas-gallery">
            {isLoading && <h3>{message}</h3>}
            <button onClick={handleNewCanvas}>New Canvas</button>
            <table>
                <thead>
                    <tr><th>Name</th><th>Template</th><th>Created At</th></tr>
                </thead>
                <tbody>                
                {
                    canvasList.map((item) => {
                        return(
                            <tr key={item.id}>
                                <td><a href={`/canvas/${item.id}`}>{item.name}</a></td>
                                <td>{item.template}</td>
                                <td>{item.createdAt.toString()}</td>
                            </tr>
                        )
                    })
                }
                </tbody>
            </table>
        </div>
    )
}

export default CanvasGallery