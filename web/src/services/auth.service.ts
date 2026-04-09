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
    private cachedUser: User | null = null;

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

        // Кешируем данные пользователя
        if (response.data.user) {
            this.cachedUser = response.data.user;
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

        // При обновлении токена сбрасываем кеш пользователя
        // Он будет обновлен при следующем запросе
        this.cachedUser = null;

        return response.data;
    }

    /**
     * Выход из системы
     */
    async logout(): Promise<LogoutResponse | void> {
        try {
            const response = await apiClient.getClient().post<LogoutResponse>(
                '/v1/auth/logout'
            );
            return response.data;
        } catch (error) {
            // Игнорируем ошибки - главное очистить токен локально
            console.warn('Logout request failed, but clearing local token:', error);
        } finally {
            // Всегда очищаем токен и кеш локально
            apiClient.clearAccessToken();
            this.cachedUser = null;
        }
    }

    /**
     * Получение информации о текущем пользователе
     * Использует кеширование для предотвращения повторных запросов
     */
    async getCurrentUser(forceRefresh: boolean = false): Promise<User> {
        // Если есть кеш и не требуется принудительное обновление - возвращаем его
        if (this.cachedUser && !forceRefresh) {
            return this.cachedUser;
        }

        // Запрашиваем данные с сервера
        const response = await apiClient.getClient().get<User>('/v1/auth/me');
        this.cachedUser = response.data;
        return response.data;
    }

    /**
     * Сброс кеша пользователя
     * Полезно когда нужно принудительно обновить данные
     */
    invalidateCache(): void {
        this.cachedUser = null;
    }

    /**
     * Проверка, авторизован ли пользователь
     */
    isAuthenticated(): boolean {
        return apiClient.getAccessToken() !== null;
    }

    /**
     * Получить кешированные данные пользователя (если есть)
     */
    getCachedUser(): User | null {
        return this.cachedUser;
    }
}

// Создаем и экспортируем единственный экземпляр сервиса
export const authService = new AuthService();
export default authService;
