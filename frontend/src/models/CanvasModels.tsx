export interface CanvasSubmission {
    name: string;
    template: string;
    data: CanvasData;
    visibility: string;
    orgId?: string | null;
    groupId?: string | null;
}

export interface StoredCanvas {
    id: string
    name: string;
    template: string;
    data: CanvasData;
    visibility: string;
    orgId?: string | null;
    groupId?: string | null;
    createdAt: Date
}

export interface ShapesType {
    id?: string
    tool: string;
    location: { x: number; y: number; };
}

export interface LinesType {
    id?: string
    tool: string;
    points: number[];
}

export interface CanvasData {
    lines: LinesType[];
    shapes: ShapesType[];
}
export interface CanvasMeta {
    name: string;
    template: string;
    visibility: string;
    org_id?: string | null;
    group_id?: string | null;
}

