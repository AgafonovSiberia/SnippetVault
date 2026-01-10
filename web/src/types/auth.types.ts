/**
 * Authentication Types
 * Типы данных для работы с API авторизации
 */

export interface User {
    id: string;
    display_name: string | null;
    avatar_url: string | null;
    created_at: string;
}

export interface AuthTokens {
    access_token: string;
    token_type: string;
}

export interface AuthResponse {
    user: User;
    access_token: string;
    token_type: string;
}

export interface YandexAuthRequest {
    token: string;
}

export interface TokenResponse {
    access_token: string;
    token_type: string;
}

export interface RefreshTokenRequest {
    refresh_token?: string;
}

export interface LogoutResponse {
    message: string;
}
