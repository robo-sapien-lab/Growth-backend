import React, { createContext, useState, ReactNode, useEffect } from 'react';
import * as SecureStore from 'expo-secure-store';
import jwtDecode from 'jwt-decode';
import { login as loginApi, signup as signupApi } from '../api/auth';

interface AuthContextProps {
  token: string | null;
  userId: number | null;
  /**
   * Logs the user in and resolves to true on success.
   */
  login: (email: string, password: string) => Promise<boolean>;
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
  login: async () => false,
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

  const login = async (email: string, password: string): Promise<boolean> => {
    try {
      const tokenVal = await loginApi(email, password);
      await SecureStore.setItemAsync('token', tokenVal);
      setToken(tokenVal);
      const decoded: any = jwtDecode(tokenVal);
      setUserId(decoded.user_id);
      return true;
    } catch (e) {
      return false;
    }
  };

  const signup = async (data: SignupData) => {
    await signupApi(data);
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
