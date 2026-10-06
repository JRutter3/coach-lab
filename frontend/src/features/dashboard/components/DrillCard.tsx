import type { StoredCanvas } from "../../../models/CanvasModels"
import logoImage from "../../../assets/CoachLabLogo.jpeg"

interface DrillCardProps {
    drill: StoredCanvas
    onDelete: (drillId: string) => void 
    onEdit: (drillId: string) => void 
}
const DrillCard = ( { drill, onDelete, onEdit }: DrillCardProps) => {
    return (
        <article className="drill-card">
            <div className="card-preview">
                <img src={logoImage} alt={drill.name}/>
            </div>
            <div className="card-body">
                <h3>{drill.name}</h3>
                <div className="drill-meta">
                    <p>{drill.template}</p>
                    <p>{drill.createdAt.toString()}</p>
                </div>
            </div>

            <div className="card-actions">
                <button
                    className="gallery-btn"
                    type="button"
                    onClick={() => onEdit(drill.id)}
                >
                    Edit Drill
                </button>
                <button
                    className="gallery-btn-grey btn-danger"
                    type="button"
                    onClick={() => onDelete(drill.id)}
                >
                    🗑️
                </button>
            </div>
        </article>
    )
}

export default DrillCard