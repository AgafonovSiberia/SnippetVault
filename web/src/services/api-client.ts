import axios from 'axios';
import type { AxiosInstance, AxiosError, InternalAxiosRequestConfig } from 'axios';

/**
 * API Client Configuration
 * Настройка Axios клиента для работы с backend API
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

export class ApiClient {
    private client: AxiosInstance;
    private accessToken: string | null = null;

    constructor() {
        // Загружаем токен из LocalStorage при инициализации
        if (typeof window !== 'undefined') {
            this.accessToken = localStorage.getItem('access_token');
        }

        this.client = axios.create({
            baseURL: API_BASE_URL,
            timeout: 10000,
            headers: {
                'Content-Type': 'application/json',
            },
            withCredentials: true, // Для работы с cookies (refresh_token)
        });

        this.setupInterceptors();
    }

    /**
     * Настройка перехватчиков запросов и ответов
     */
    private setupInterceptors(): void {
        // Перехватчик запросов - добавляем access_token
        this.client.interceptors.request.use(
            (config: InternalAxiosRequestConfig) => {
                if (this.accessToken && config.headers) {
                    config.headers.Authorization = `Bearer ${this.accessToken}`;
                }
                return config;
            },
            (error: AxiosError) => {
                return Promise.reject(error);
            }
        );

        // Перехватчик ответов - обработка ошибок и обновление токена
        this.client.interceptors.response.use(
            (response) => response,
            async (error: AxiosError) => {
                const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean };

                // Не пытаемся обновлять токен для самого endpoint refresh
                if (originalRequest.url?.includes('/auth/refresh')) {
                    // Если refresh не удался - очищаем токен и редиректим
                    this.clearAccessToken();
                    if (window.location.pathname !== '/') {
                        window.location.href = '/';
                    }
                    return Promise.reject(error);
                }

                // Если получили 401 и это не повторный запрос
                if (error.response?.status === 401 && !originalRequest._retry) {
                    originalRequest._retry = true;

                    try {
                        // Пытаемся обновить токен
                        const response = await this.client.post('/v1/auth/refresh');
                        const newAccessToken = response.data.access_token;

                        this.setAccessToken(newAccessToken);

                        // Повторяем оригинальный запрос с новым токеном
                        if (originalRequest.headers) {
                            originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
                        }
                        return this.client(originalRequest);
                    } catch (refreshError) {
                        // Если обновление токена не удалось - очищаем токен и перенаправляем на логин
                        this.clearAccessToken();
                        if (window.location.pathname !== '/') {
                            window.location.href = '/';
                        }
                        return Promise.reject(refreshError);
                    }
                }

                return Promise.reject(error);
            }
        );
    }

    /**
     * Установка access токена
     */
    public setAccessToken(token: string): void {
        this.accessToken = token;
        if (typeof window !== 'undefined') {
            localStorage.setItem('access_token', token);
        }
    }

    /**
     * Получение сохраненного access токена
     */
    public getAccessToken(): string | null {
        if (!this.accessToken && typeof window !== 'undefined') {
            this.accessToken = localStorage.getItem('access_token');
        }
        return this.accessToken;
    }

    /**
     * Очистка access токена
     */
    public clearAccessToken(): void {
        this.accessToken = null;
        if (typeof window !== 'undefined') {
            localStorage.removeItem('access_token');
        }
    }

    /**
     * Получение экземпляра Axios клиента
     */
    public getClient(): AxiosInstance {
        return this.client;
    }
}

// Создаем и экспортируем единственный экземпляр клиента
export const apiClient = new ApiClient();
export default apiClient;
