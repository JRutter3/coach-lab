import React, { useEffect, useRef, useState } from "react"
import CanvasDrawingArea, { type CanvasHandle } from "./CanvasDrawingArea"
import CanvasMetaForm from "./CanvasMetaForm";
import { type CanvasMeta, type CanvasData, type CanvasSubmission, type StoredCanvas } from "../../../models/CanvasModels";
import Palette from "./Palette";
import axios from "axios";
import "./CanvasEditor.css"

const submitCanvasPayload = async (
    canvasMetaData: CanvasMeta,
    canvasData: CanvasData,
    canvasId: string,
) => {
    const payload: CanvasSubmission = {
        ...canvasMetaData, data: canvasData
    }
    try {
        await axios.put(
            `/api/v1/canvas-drawing/${canvasId}`,
            payload,
            {
                withCredentials: true,
                headers: {"Content-Type": "application/json"},
            }
        )
    } catch (err) {
        console.error("An error occurred updating canvas data: ", err)
    }
}

const CanvasEditor = ({canvasId}: {canvasId: string}) => {
    const [activeTool, toolSetter] = useState("brush")
    const [canvasMeta, setCanvasMeta] = useState<CanvasMeta>({ name: "", template: "", visibility: "" })
    const [initialData, setInitialData] = useState<CanvasData | null>(null);
    const [isLoading, setIsLoading] = useState(false)
    const canvasRef = useRef<CanvasHandle>(null);

    // Fetch initial data:
    console.log("Loading page for canvas data: ", canvasId)

    useEffect(() => {
        setIsLoading(true)
        const fetchCanvas = async () => {
            console.log("Fetching canvas...")
            try {
                const resp = await axios.get(
                    `/api/v1/canvas-drawing/${canvasId}/`,
                    { withCredentials: true }
                )
                console.log("Data loaded: ", resp.data)
                const data: StoredCanvas = resp.data
                setCanvasMeta({
                    name: data.name,
                    template: data.template,
                    visibility: data.visibility,
                    org_id: data.orgId,
                    group_id: data.groupId
                })

                const canvasData: CanvasData = {
                    lines: data.data.lines.map((line) => (
                        { ...line, id: `line-${crypto.randomUUID()}` }
                    )
                    ),
                    shapes: data.data.shapes.map((shape) => (
                        { ...shape, id: `shape-${crypto.randomUUID()}` }
                    ))
                }

                setInitialData(canvasData)

            } catch (err) {
                console.error("Failed to load canvas data:", err)
            } finally {
                setIsLoading(false)
            }
        }
        fetchCanvas().then(() => { console.log("Canvas loaded") })
    }, [canvasId])

    const onClear = (e: React.MouseEvent) => {
        const blankCanvas: CanvasData = {
            lines: [],
            shapes: [],
        }
        setInitialData(blankCanvas)
    }
    const onSubmit = async (e: React.SubmitEvent) => {
        console.log("Submitting data...")
        e.preventDefault()
        const canvasData = canvasRef.current?.getCanvasData();
        if (!canvasData){
            console.log("No canvasData found...")
            return;
        } 
        console.log("Got canvas data", canvasData)
        await submitCanvasPayload(canvasMeta, canvasData, canvasId)
    }

    if (isLoading) return <div>Loading editor...</div>;

    return (
        <form onSubmit={onSubmit} className="canvas-editor">
            <div className="canvas-editor__meta">
                <CanvasMetaForm value={canvasMeta} onChange={setCanvasMeta} />
            </div>
            <div className="canvas-editor__workspace">
                <Palette activeTool={activeTool} toolSetter={toolSetter} />
                <CanvasDrawingArea ref={canvasRef} tool={activeTool} initialData={initialData} />
            </div>
            <div className="canvas-editor__actions">
                <button type="submit">Submit</button>
                <button type="button" onClick={onClear}>Clear</button>
            </div>
        </form>
    )
}

export default CanvasEditor
