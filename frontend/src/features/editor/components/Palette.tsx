import "./Palette.css"


interface PaletteProps {
    activeTool: string
    toolSetter: (toolKey: string) => void
}
interface Tool {
    id: string
    label: string
    icon: string
}

interface ToolGroup {
    label: string
    tools: Tool[]
}

const toolGroups: ToolGroup[] = [
    {
        label: "Markers",
        tools: [
            {id: "circle", label: "Circle", icon: "⭕"},
            {id: "x-mark", label: "X Mark", icon: "❌"},
        ]
    },
    {
        label: "Drawing",
        tools: [
            {id: "brush", label: "Brush", icon: "🖌️"},
            {id: "eraser", label: "Eraser", icon: "🧼"},
        ]
    }
]

const Palette = ( {activeTool, toolSetter}: PaletteProps ) => {

    return (
        <aside className="palette">
            {toolGroups.map((group) => (
                <div key={group.label} className="palette__group">
                    <span className="palette__group-label">{group.label}</span>
                    <div className="palette__grid">
                        {group.tools.map((tool) => {
                            const isActive = tool.id === activeTool
                            return (
                                <button
                                    type="button"
                                    key={tool.id}
                                    className={`palette__tool-btn ${isActive ? "palette__tool-btn--active": ""}`}
                                    onClick={() => toolSetter(tool.id)}
                                    title={tool.label}
                                    aria-label={tool.label}
                                    aria-pressed={isActive}
                                >
                                    <span className="palette__tool-icon">{tool.icon}</span>
                                </button>
                            )
                        })}
                    </div>
                </div>
            ))}
        </aside>
    )
}

export default Palette