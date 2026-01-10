import { apiClient } from './api-client';
import type {
    AuthResponse,
    YandexAuthRequest,
    TokenResponse,
    LogoutResponse,
    User
} from '../types/auth.types';

/**
 * Auth Service
 * Сервис для работы с авторизацией
 */

export class AuthService {
    /**
     * Авторизация через Yandex ID
     * @param token - JWT токен от Yandex ID
     */
    async authenticateYandex(token: string): Promise<AuthResponse> {
        const requestData: YandexAuthRequest = { token };
        const response = await apiClient.getClient().post<AuthResponse>(
            '/v1/auth/yandex',
            requestData
        );

        // Сохраняем access токен
        if (response.data.access_token) {
            apiClient.setAccessToken(response.data.access_token);
        }

        return response.data;
    }

    /**
     * Обновление access токена
     */
    async refreshToken(): Promise<TokenResponse> {
        const response = await apiClient.getClient().post<TokenResponse>(
            '/v1/auth/refresh'
        );

        if (response.data.access_token) {
            apiClient.setAccessToken(response.data.access_token);
        }

        return response.data;
    }

    /**
     * Выход из системы
     */
    async logout(): Promise<LogoutResponse> {
        const response = await apiClient.getClient().post<LogoutResponse>(
            '/v1/auth/logout'
        );

        apiClient.clearAccessToken();

        return response.data;
    }

    /**
     * Получение информации о текущем пользователе
     */
    async getCurrentUser(): Promise<User> {
        const response = await apiClient.getClient().get<User>('/v1/auth/me');
        return response.data;
    }

    /**
     * Проверка, авторизован ли пользователь
     */
    isAuthenticated(): boolean {
        return apiClient.getAccessToken() !== null;
    }
}

// Создаем и экспортируем единственный экземпляр сервиса
export const authService = new AuthService();
export default authService;
