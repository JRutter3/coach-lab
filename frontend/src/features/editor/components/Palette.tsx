
interface PaletteProps {
    activeTool: string
    toolSetter: (toolKey: string) => void
}

const Palette = ( {activeTool, toolSetter}: PaletteProps ) => {
    const handleToolSelect = (toolId: string) => {
        toolSetter(toolId)
    }

    const tools = [
        {
            id: "circle",
            label: "O",
            icon: "⭕"
        },
        {
            id: "x-mark",
            label: "X",
            icon: "❌"
        },
        {
            id: "brush",
            label: "Brush",
            icon: "🖌️"
        },
        {
            id: "eraser",
            label: "Eraser",
            icon: "🧼"
        },
    ]

    return (
        <aside
            className="tool-pallette"
            style={{ width: 180 }}
        >
            {tools.map((tool) => {
                const isActive = tool.id === activeTool
                return (
                    <button
                        type="button"
                        key={tool.id}
                        className="tool-btn"
                        onClick={() => handleToolSelect(tool.id)}
                        style={{
                            backgroundColor: isActive ? '#007acc' : '#2d2d2d',
                            border: isActive ? '1px solid #0098ff' : '1px solid #444'
                        }}
                    >
                        <span>{tool.icon}</span>
                        <span>{tool.label}</span>
                    </button>
                )
            })}
        </aside>
    )
}

export default Palette