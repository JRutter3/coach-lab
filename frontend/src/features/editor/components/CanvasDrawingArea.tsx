import { forwardRef, useEffect, useImperativeHandle, useRef } from 'react';
import type { CanvasData, LinesType, ShapesType } from '../../../models/CanvasModels';
import Konva from 'konva';
import { type KonvaEventObject } from 'konva/lib/Node';
import { Image, Layer, Stage } from "react-konva";
import fullRinkImage from '../../../assets/HocekyFull.png'
import useImage from 'use-image';
import { _ZodString } from 'zod';


export interface CanvasHandle{
    getCanvasData: () => CanvasData | null;
}

interface CanvasProps {
    tool: string
    initialData: CanvasData | null
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

const konvaRingFromShapesType = (shape: ShapesType) => {
    return  new Konva.Ring({
        id: `shape-${shape.id}`,
        x: shape.location.x,
        y: shape.location.y,
        outerRadius: 10,
        innerRadius: 5,
        fill: "black"
    });
}

const konvaLineFromLineType = (line: LinesType) => {
    return new Konva.Line({
        id: `line-${line.id}`,
        points: line.points,
        stroke: "#df4b26",
        strokeWidth: 5,
        tension: 0.5,
        lineCap: "round",
        lineJoin: "round",
        globalCompositeOperation: line.tool === 'eraser' ? 'destination-out' : 'source-over'
});

}

const CanvasDrawingArea = forwardRef<CanvasHandle, CanvasProps>(
    ({tool, initialData}: {tool:string, initialData: CanvasData | null}, ref) => {
        const stageRef = useRef<Konva.Stage>(null); 
        const layerRef = useRef<Konva.Layer>(null);
        // Live vector data refs (no re-rendering)
        const sceneDataRef = useRef<CanvasData>({lines:[], shapes:[]});
        const isDrawing = useRef(false);


        // Load initial state into konva once
        useEffect(() => {
            if (!initialData || !layerRef.current) return;
            const layer = layerRef.current;
            layer.destroyChildren();  // Clear existing

            // Store initial data in ref
            sceneDataRef.current = initialData;

            //Draw all the lines: 
            initialData.lines.forEach((line) => {
                const lineNode = konvaLineFromLineType(line)
                layer.add(lineNode)
            });

            // Draw all the shapes:
            initialData.shapes.forEach((shape) => {
                if (shape.tool === "circle"){  // TODO: Add support for different shapes
                    const shapeNode = konvaRingFromShapesType(shape)
                    layer.add(shapeNode);
                }
            });

            layer.batchDraw();
        }, [initialData]);


        const handleMouseDown = (e: KonvaEventObject<MouseEvent | TouchEvent>) => {

            const pos = e.target.getStage()?.getPointerPosition();
            if (!pos || !layerRef.current) return;
            
            switch (tool) {
                case "eraser":
                    isDrawing.current = true;
                    return;

                case "circle": 
                    const newShape: ShapesType = {
                        id: crypto.randomUUID(),
                        tool: "circle",
                        location: {x: pos.x, y: pos.y}
                    };

                    sceneDataRef.current.shapes.push(newShape);
                    const ringNode = konvaRingFromShapesType(newShape)
                    layerRef.current.add(ringNode)
                    layerRef.current.batchDraw()
                    return;

                case "brush":
                    isDrawing.current=true
                    const newLine: LinesType = {
                        id: crypto.randomUUID(),
                        tool: tool,
                        points: [pos.x, pos.y, pos.x, pos.y]
                    }
                    sceneDataRef.current.lines.push(newLine);

                    const lineNode = konvaLineFromLineType(newLine)
                    layerRef.current.add(lineNode)
                    layerRef.current.batchDraw()
                    return;

                case "default":
                    throw new Error(`Unknown tool selection: ${tool}`)
            }
        }

        const handleMouseMove = (e: Konva.KonvaEventObject<MouseEvent>) => {
            if (!isDrawing.current) return;
            const pos = e.target.getStage()?.getPointerPosition();
            if (!pos || !layerRef.current) return;
            switch (tool) {
                case "brush":
                    const lines = sceneDataRef.current.lines;
                    const currentLine = lines[lines.length - 1];
                
                    currentLine.points = currentLine.points.concat([pos.x, pos.y]);
                    
                    const children = layerRef.current.getChildren();
                    const lastKonvaLine = children[children.length - 1] as Konva.Line;

                    if (lastKonvaLine) {
                        lastKonvaLine.points(currentLine.points);
                        layerRef.current.batchDraw();
                    }
                    return;
                case "eraser":
                    // Find the bad lines and shapes...
                    const badLines = sceneDataRef.current.lines.filter(
                        (line) => line.points.some(
                            (_, i) => i % 2 === 0 // We process i & i+1, so skip odd is
                            && isPointNear(
                                line.points[i],
                                line.points[i+1],
                                pos.x,
                                pos.y,
                                ERASER_RADIUS
                            )
                        )
                    )
                    const badShapes = (
                        sceneDataRef.current.shapes.filter(
                            (shape) => isPointNear(
                                shape.location.x,
                                shape.location.y,
                                pos.x,
                                pos.y,
                                ERASER_RADIUS
                            )
                        )
                    );

                    // Get the IDs from those bad lines and shapes
                    const badShapeIds = new Set(badShapes.map((s) => s.id));
                    const badLineIds = new Set(badLines.map((l) => l.id));


                    // Drop the bad shapes from the referenced lines / shapes
                    sceneDataRef.current.lines = sceneDataRef.current.lines.filter(
                        (l) => !badLineIds.has(l.id)
                    );
                    sceneDataRef.current.shapes = sceneDataRef.current.shapes.filter(
                        (s) => !badShapeIds.has(s.id)
                    );

                    // Drop the nodes of the bad lines / shapes from the layer
                    const layer = layerRef.current;
                    if (layer) {
                        badLineIds.forEach((badId) => {
                            const node = layer.findOne(`#line-${badId}`);
                            node?.destroy();
                        });
                        badShapeIds.forEach((badId) => {
                            const node = layer.findOne(`#shape-${badId}`);
                            node?.destroy();
                        });
                        layer.batchDraw()
                    }
                    return;
            }
        }

        const handleMouseUp = () => isDrawing.current = false;

        useImperativeHandle(ref, () => {
            return {getCanvasData: () => sceneDataRef.current,}
        });

        return (
            <div className="canvas-workspace">
                <Stage
                    ref={stageRef}
                    width={1000}
                    height={500}
                    onMouseDown={handleMouseDown}
                    onMouseMove={handleMouseMove}
                    onMouseUp={handleMouseUp}
                >
                    <Layer ref={layerRef}>
                        {initialData && <URLImage src={fullRinkImage} width={1000} />}
                    </Layer>
                    <Layer ref={layerRef} />
                </Stage>
            </div>

        );
    }
);
    
export default CanvasDrawingArea