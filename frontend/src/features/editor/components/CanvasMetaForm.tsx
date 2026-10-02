import type React from "react";
import type { CanvasMeta } from "../../../models/CanvasModels";


interface CanvasMetaFormProps {
    value: CanvasMeta;
    onChange: React.Dispatch<React.SetStateAction<CanvasMeta>>;
}

const CanvasMetaForm = ({value, onChange}: CanvasMetaFormProps)=> {
    return(
        <fieldset>
            <legend className="sr-only">Canvas Info</legend>
            <div className="field-group">
                <label htmlFor="canvas-name">Name</label>
                <input
                    id="canvas-name"
                    type="text"
                    value={value.name}
                    onChange={(e) => onChange((prev) => ({...prev, name: e.target.value}))}
                />
                <label htmlFor="template">Template</label>
                <select
                    id="template" value="full_ice_rink"
                    onChange = {(e) => onChange((prev) => ({...prev, template: e.target.value}))}
                >
                    <option value="full_ice_rink" >Full Ice Rink</option>
                </select>
                <label htmlFor="visibility">Visibility</label>
                <select
                    id="visibility"
                    value="private"
                    onChange={
                        (e) => onChange((prev) => ({ ...prev, visibility: e.target.value}))
                    }
                >
                    <option value="private">Private</option>
                </select>
            </div>
        </fieldset>
    )
}
export default CanvasMetaForm