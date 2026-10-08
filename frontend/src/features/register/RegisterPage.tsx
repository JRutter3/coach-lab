import axios from "axios"
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

interface RegistrationData {
    email: string
    password: string
    firstName: string
    lastName: string
}
const RegistrationForm = () => {
    const [formData, setFormData] = useState<RegistrationData>(
        {email: "", password: "", firstName: "", lastName: ""}
    )
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null)
    const navigate = useNavigate()
    const handleSubmit = async (e: React.SubmitEvent) => {
        e.preventDefault()
        setLoading(true)
        setError(null)

        try {
            const res = await axios.post(
                "/api/v1/users",
                formData,
                {
                    headers: {"Content-Type": "application/json"},
                    withCredentials: true
                }
            )

            if ((res.status === 422)) {
                setError("Malformed request")
                return
            }

            navigate("/")
        } catch {
            setError("Something went wrong. Please try again")
        } finally {
            setLoading(false)
        }
    }

    return (
        <form onSubmit={handleSubmit}>
            <input 
                type="text"
                value={formData.firstName}
                onChange={
                    (e) => setFormData({...formData, "firstName": e.target.value})
                }
                placeholder="First Name"
                required
            />
            <input
                type="text"
                value={formData.lastName}
                onChange={
                    (e) => setFormData({...formData, "lastName": e.target.value})
                }
                placeholder="Last Name"
                required
            />  
            <input 
                type="email"
                value={formData.email}
                onChange={(e) => setFormData({...formData, "email": e.target.value})}
                placeholder="Email"
                required
            />
            <input
                type="password"
                value={formData.password}
                onChange={(e) => setFormData({...formData, "password": e.target.value})}
                placeholder="Password"
                required
            />
            { error && <p className = "error">{error}</p> }
            <button type="submit" disabled={loading}>
                {loading ? "Registering User...": "Register"}
            </button>
        </form>
    )
}

export default RegistrationForm