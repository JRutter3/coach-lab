import axios from 'axios'
import React from 'react';
import { Stage, Layer, Line, Image, Ring} from 'react-konva'
import { type KonvaEventObject } from 'konva/lib/Node'
import useImage from 'use-image'
import imageSource from '../assets/HocekyFull.png'

interface LinesType {
    tool: string,
    points: number[] 
}

interface ShapesType {
    tool: string
    location: {x: number, y: number}
}

interface CanvasSubmission {
    template: string
    lines: LinesType[]
    shapes: ShapesType[]
}

const ERASER_RADIUS = 10;

const isPointNear= (
    px: number, py: number, cx: number, cy: number, radius: number
): boolean => {
    const dx = px - cx;
    const dy = py - cy;
    return Math.sqrt(dx * dx + dy * dy) < radius;  // Pythagoras! 

};

const URLImage = ({ src, ...rest}: { src: string, [key: string]: any }) => {
    const [image] = useImage(src, 'anonymous')
    return <Image image={image} {...rest} />;
}

const Canvas = ( {tool}: {tool: string} ) => {
    const [lines, setLines] = React.useState<LinesType[]>([])
    const [shapes, setShapes] = React.useState<ShapesType[]>([])
    const isDrawing = React.useRef(false)
    const eraserPoints = React.useRef<number[]>([])

    const handleMouseDown = (e: KonvaEventObject<MouseEvent | TouchEvent>) => {
        const stage = e.target.getStage();
        if (!stage) return;
        const pos = stage.getPointerPosition();
        if (!pos) return;
        
        switch (tool) {
            case "eraser":
                isDrawing.current = true;
                return;
            case "brush":
                isDrawing.current=true
                console.log("Stage set to variable", stage)

                if (pos) {
                    // console.log("Setting line point to current mouse position", pos)
                    setLines([...lines, { tool, points: [pos.x, pos.y]}]);
                } else {
                    // console.log("Pointer position returned falsy result", pos)
                }
                return;

            case "circle": 
                setShapes([...shapes, {tool, location: pos}])
                return;
            case "default":
                throw new Error(`Unknown tool selection: ${tool}`)
        }
    }

    const handleMouseMove = (e: KonvaEventObject<MouseEvent | TouchEvent>) => {
        // If we aren't currently drawing, then just return.
        if (!isDrawing.current) return;
        e.evt.preventDefault();
        const stage = e.target.getStage();
        if (!stage) return;
        const point = stage.getPointerPosition()
        if (!point) return;

        switch (tool) {
            case "eraser":
                setLines((prev) =>
                    // NOTE: the points end up in a single array, so we grab the evens (i % 2) and then process points[i] (x coord) and points[i+1] (y coord)
                    prev.filter((line) => 
                        !line.points.some((_, i) =>
                            i % 2 === 0 &&
                            isPointNear(line.points[i], line.points[i+1], point.x, point.y, ERASER_RADIUS)
                        )
                    )
                );
                setShapes((prev) => 
                    prev.filter(
                        (shape) => !isPointNear(shape.location.x, shape.location.y, point.x, point.y, ERASER_RADIUS * 2)
                    )
                );
                return;


            case "brush":
                // Now draw the line
                let lastLine = lines[lines.length - 1];
                lastLine.points = lastLine.points.concat([point.x, point.y])
                
                // Replace the last line
                lines.splice(lines.length - 1, 1, lastLine);
                setLines(lines.concat())
                return
            case "default":
                throw new Error(`Unknown tool selection: ${tool}`)
        }
    };

    const handleMouseUp = () => {
        if (tool === "eraser" && eraserPoints.current.length > 0) {

        }
        isDrawing.current = false;
    };

    const handleSubmitClick = async () => {
        const payload: CanvasSubmission = {
            template: "full_hockey_rink",
            lines,
            shapes
        }
        console.log("Submitting Canvas", payload)
        try {
            const response = await axios.post('http://localhost:8000/api/v1/canvas-drawing', payload)
            console.log('Success:', response.data);
        } catch (error) {
            if (axios.isAxiosError(error)){
            console.error('Axios error:', error.response?.data || error.message)
            } else {
                console.error("Unexpected error:", error);
            }
        }

    }
    const handleClearClick = () => {
        setLines([])
        setShapes([])
    }
    return (
        
        <>
            <div className="canvas-workspace">
            <Stage
                width={1000}
                height={500}
                onMouseDown={handleMouseDown}
                onMouseMove={handleMouseMove}
                onMouseUp={handleMouseUp}
                onTouchStart={handleMouseDown}
                onTouchEnd={handleMouseUp}
                onTouchMove={handleMouseMove}
            >
                <Layer>
                    <URLImage
                        src={imageSource}
                        width={1000}
                    />
                </Layer>
                <Layer>
                    {lines.map((line, i) => (
                        <Line
                            key={i}
                            points={line.points}
                            stroke="#df4b26"  // color of brush
                            strokeWidth={5}
                            tension={0.5}
                            lineCap="round"
                            lineJoin="round"
                            globalCompositeOperation={
                                line.tool === 'eraser' ? 'destination-out' : 'source-over'
                            }
                        />
                    ))}
                </Layer>
                <Layer>
                    {shapes.map((shape, i) => (
                        <Ring
                            key={i}
                            x={shape.location.x}
                            y={shape.location.y}
                            outerRadius={10}
                            innerRadius={5}
                            fill="black"
                        />
                    ))}
                </Layer>
            </Stage>
            <button
                onClick={handleClearClick}
            >Clear</button>
            <button
                onClick={handleSubmitClick}
            >Submit</button>
            </div>
        </>
    )
}

export default Canvas