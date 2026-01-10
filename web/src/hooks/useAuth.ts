import { useState, useEffect, useCallback } from 'react';
import { authService } from '../services/auth.service';
import type { User, AuthResponse } from '../types/auth.types';

/**
 * Hook для работы с авторизацией
 */

interface UseAuthReturn {
    user: User | null;
    isAuthenticated: boolean;
    isLoading: boolean;
    error: string | null;
    login: (token: string) => Promise<void>;
    logout: () => Promise<void>;
    refreshUser: () => Promise<void>;
}

export const useAuth = (): UseAuthReturn => {
    const [user, setUser] = useState<User | null>(null);
    const [isLoading, setIsLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    /**
     * Инициализация - проверка авторизации
     */
    useEffect(() => {
        const initAuth = async () => {
            try {
                if (authService.isAuthenticated()) {
                    const userData = await authService.getCurrentUser();
                    setUser(userData);
                }
            } catch (err) {
                console.error('Failed to initialize auth:', err);
                // Если не удалось получить пользователя, очищаем токен
                authService.logout();
            } finally {
                setIsLoading(false);
            }
        };

        initAuth();
    }, []);

    /**
     * Авторизация через Yandex ID
     */
    const login = useCallback(async (token: string) => {
        setIsLoading(true);
        setError(null);

        try {
            const response: AuthResponse = await authService.authenticateYandex(token);
            setUser(response.user);
        } catch (err) {
            const errorMessage = err instanceof Error ? err.message : 'Authentication failed';
            setError(errorMessage);
            throw err;
        } finally {
            setIsLoading(false);
        }
    }, []);

    /**
     * Выход из системы
     */
    const logout = useCallback(async () => {
        setIsLoading(true);
        setError(null);

        try {
            await authService.logout();
            setUser(null);
        } catch (err) {
            const errorMessage = err instanceof Error ? err.message : 'Logout failed';
            setError(errorMessage);
            console.error('Logout error:', err);
        } finally {
            setIsLoading(false);
        }
    }, []);

    /**
     * Обновление данных пользователя
     */
    const refreshUser = useCallback(async () => {
        setIsLoading(true);
        setError(null);

        try {
            const userData = await authService.getCurrentUser();
            setUser(userData);
        } catch (err) {
            const errorMessage = err instanceof Error ? err.message : 'Failed to refresh user data';
            setError(errorMessage);
            throw err;
        } finally {
            setIsLoading(false);
        }
    }, []);

    return {
        user,
        isAuthenticated: !!user,
        isLoading,
        error,
        login,
        logout,
        refreshUser,
    };
};

export default useAuth;
