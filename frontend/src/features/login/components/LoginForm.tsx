import "../../../App.css"
import axios from "axios";
import React, { useState } from "react";

const LoginForm = () => {
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [error, setError] = useState<string | null>(null)
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e: React.SubmitEvent) => {
        e.preventDefault();
        setLoading(true)
        setError(null)

        try {
            const res = await axios.post(
                "/api/login/",
                { "email": email, "password": password},
                {
                    "headers": {"Content-Type": "application/json"},
                    "withCredentials": true
                }
            )

            if (!(res.status === 200)) {
                setError("Invalid email or password")
                return
            }

            window.location.href = "/dashboard"
        } catch {
            setError("Something went wrong. Please try again.")
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="login-container">
            <form onSubmit={handleSubmit} className="login-form">
                <div className="form-group">
                    <label htmlFor="email-input">E-Mail</label>
                    <input
                        id="email-input"
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="Email"
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="password-input">Password</label>
                    <input
                        id="password-input"
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Password"
                        required
                    />
                </div>
                { error && <p className="error">{error}</p> }
                <div className="form-actions">
                    <button type="submit" disabled={loading} className='btn-primary'>
                        {loading ? "Signing in..." : "Sign in"}
                    </button>
                    <button className="btn-secondary" type="button" onClick={() => window.location.href="/register"}>
                        Sign-Up
                    </button>
                </div>
            </form>
        </div>
    )
}

export default LoginForm