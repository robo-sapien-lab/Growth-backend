import React, { createContext, useState, ReactNode, useEffect } from 'react';
import * as SecureStore from 'expo-secure-store';
import jwtDecode from 'jwt-decode';

interface AuthContextProps {
  token: string | null;
  userId: number | null;
  login: (email: string, password: string) => Promise<void>;
  signup: (data: SignupData) => Promise<void>;
  logout: () => void;
}

interface SignupData {
  name: string;
  email: string;
  password: string;
  grade: string;
  school_code: string;
}

const AuthContext = createContext<AuthContextProps>({
  token: null,
  userId: null,
  login: async () => {},
  signup: async () => {},
  logout: () => {},
});

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [token, setToken] = useState<string | null>(null);
  const [userId, setUserId] = useState<number | null>(null);

  useEffect(() => {
    const loadToken = async () => {
      const stored = await SecureStore.getItemAsync('token');
      if (stored) {
        setToken(stored);
        const decoded: any = jwtDecode(stored);
        setUserId(decoded.user_id);
      }
    };
    loadToken();
  }, []);

  const login = async (email: string, password: string) => {
    const res = await fetch('http://localhost:8000/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });
    const data = await res.json();
    setToken(data.access_token);
    await SecureStore.setItemAsync('token', data.access_token);
    const decoded: any = jwtDecode(data.access_token);
    setUserId(decoded.user_id);
  };

  const signup = async (data: SignupData) => {
    await fetch('http://localhost:8000/auth/signup', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
  };

  const logout = async () => {
    setToken(null);
    setUserId(null);
    await SecureStore.deleteItemAsync('token');
  };

  return (
    <AuthContext.Provider value={{ token, userId, login, signup, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;
