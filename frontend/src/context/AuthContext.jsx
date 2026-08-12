import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react';
import {
  changePassword as changePasswordRequest,
  getCurrentUser,
  loginUser,
  logoutUser,
  registerUser,
  updateProfile as updateProfileRequest,
  updateSettings as updateSettingsRequest,
} from '../services/authService';
import {
  clearAuthStorage,
  getToken,
  getUser,
  setToken,
  setUser,
} from '../utils/storage';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUserState] = useState(() => getUser());
  const [token, setTokenState] = useState(() => getToken());
  const [loading, setLoading] = useState(false);
  const [initializing, setInitializing] = useState(true);

  const isAuthenticated = Boolean(token && user);

  const handleAuthSuccess = useCallback((data) => {
    setToken(data.access_token);
    setUser(data.user);
    setTokenState(data.access_token);
    setUserState(data.user);
  }, []);

  const refreshUser = useCallback(async () => {
    const profile = await getCurrentUser();
    setUser(profile);
    setUserState(profile);
    return profile;
  }, []);

  useEffect(() => {
    const bootstrapAuth = async () => {
      const storedToken = getToken();
      if (!storedToken) {
        setInitializing(false);
        return;
      }

      try {
        const profile = await getCurrentUser();
        setUser(profile);
        setUserState(profile);
        setTokenState(storedToken);
      } catch {
        clearAuthStorage();
        setTokenState(null);
        setUserState(null);
      } finally {
        setInitializing(false);
      }
    };

    bootstrapAuth();
  }, []);

  const login = useCallback(async (credentials) => {
    setLoading(true);
    try {
      const data = await loginUser(credentials);
      handleAuthSuccess(data);
      return data;
    } finally {
      setLoading(false);
    }
  }, [handleAuthSuccess]);

  const register = useCallback(async (payload) => {
    setLoading(true);
    try {
      const data = await registerUser(payload);
      handleAuthSuccess(data);
      return data;
    } finally {
      setLoading(false);
    }
  }, [handleAuthSuccess]);

  const logout = useCallback(async () => {
    try {
      if (getToken()) {
        await logoutUser();
      }
    } catch {
      // Client logout proceeds even if server call fails
    } finally {
      clearAuthStorage();
      setTokenState(null);
      setUserState(null);
    }
  }, []);

  const updateProfile = useCallback(async (payload) => {
    const profile = await updateProfileRequest(payload);
    setUser(profile);
    setUserState(profile);
    return profile;
  }, []);

  const updateSettings = useCallback(async (payload) => {
    const profile = await updateSettingsRequest(payload);
    setUser(profile);
    setUserState(profile);
    return profile;
  }, []);

  const changePassword = useCallback(async (payload) => {
    return changePasswordRequest(payload);
  }, []);

  const value = useMemo(
    () => ({
      user,
      token,
      loading,
      initializing,
      isAuthenticated,
      login,
      register,
      logout,
      refreshUser,
      updateProfile,
      updateSettings,
      changePassword,
    }),
    [
      user,
      token,
      loading,
      initializing,
      isAuthenticated,
      login,
      register,
      logout,
      refreshUser,
      updateProfile,
      updateSettings,
      changePassword,
    ]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
