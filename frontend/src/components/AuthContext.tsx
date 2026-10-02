import axios from "axios";
import { createContext, useContext, useEffect, useState } from "react";

interface User {
    id: string;
    email: string;
}

const AuthContext = createContext<{
    user: User | null;
    loading: boolean;
}>({ user: null, loading: true });

export const AuthProvider = ({ children }: { children: React.ReactNode}) => {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        axios
            .get("/api/v1/users/me", {withCredentials: true})
            .then((res) => {setUser(res.data)})
            .catch(() => {setUser(null)})
            .finally(() => setLoading(false))
    }, [])
    
    return (
        <AuthContext.Provider value={{ user, loading }}>
            {children}
        </AuthContext.Provider>
    )
}

export const useAuth = () => useContext(AuthContext)
