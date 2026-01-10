/**
 * Yandex ID SDK Integration
 * Интеграция с Yandex ID для авторизации
 * 
 * Документация: https://yandex.ru/dev/id/doc/ru/suggest/script-sdk-suggest
 */

declare global {
    interface Window {
        YaAuthSuggest?: {
            init: (
                oauthParams: {
                    client_id: string;
                    response_type: string;
                    redirect_uri: string;
                },
                tokenPageOrigin: string,
                suggestParams?: {
                    view: 'button';
                    parentId: string;
                    buttonView?: 'main' | 'additional';
                    buttonTheme?: 'light' | 'dark';
                    buttonSize?: 's' | 'm' | 'l' | 'xl';
                    buttonBorderRadius?: number;
                }
            ) => Promise<{
                status: 'ok' | 'error';
                handler?: () => Promise<{ access_token: string }>;
                code?: string;
            }>;
        };
    }
}

export interface YandexIDConfig {
    clientId: string;
    redirectUri: string;
}

/**
 * Параметры для загрузки SDK
 */
export interface YandexSDKParams {
    onload?: () => void;
}

/**
 * Загрузка Yandex ID SDK
 */
export const loadYandexIDSDK = (params: YandexSDKParams = {}): Promise<void> => {
    return new Promise((resolve, reject) => {
        // Проверяем, не загружен ли уже скрипт
        if (document.getElementById('yandex-id-sdk')) {
            resolve();
            return;
        }

        const script = document.createElement('script');
        script.id = 'yandex-id-sdk';
        script.src = 'https://yastatic.net/s3/passport-sdk/autofill/v1/sdk-suggest-with-polyfills-latest.js';
        script.async = true;

        script.onload = () => {
            if (params.onload) {
                params.onload();
            }
            resolve();
        };

        script.onerror = () => {
            reject(new Error('Failed to load Yandex ID SDK'));
        };

        document.head.appendChild(script);
    });
};

/**
 * Инициализация виджета Yandex ID
 */
export const initYandexIDWidget = async (
    containerId: string,
    config: YandexIDConfig
): Promise<void> => {
    const container = document.getElementById(containerId);

    if (!container) {
        console.error(`Container with id "${containerId}" not found`);
        throw new Error(`Container with id "${containerId}" not found`);
    }

    if (!window.YaAuthSuggest) {
        console.error('YaAuthSuggest is not loaded');
        throw new Error('YaAuthSuggest SDK is not loaded');
    }

    try {
        // Очищаем контейнер
        container.innerHTML = '';

        // Инициализируем виджет "Мгновенный вход"
        const result = await window.YaAuthSuggest.init(
            {
                client_id: config.clientId,
                response_type: 'token',
                redirect_uri: config.redirectUri,
            },
            // ВАЖНО: origin текущей страницы (без пути)
            window.location.origin
        );

        if (result.status === 'error') {
            console.error('YaAuthSuggest init error:', result.code);
            throw new Error(`YaAuthSuggest init failed: ${result.code}`);
        }

        // Вызываем handler для отображения виджета
        if (result.handler) {
            await result.handler();
            console.log('Yandex ID widget rendered successfully');

            // Виджет автоматически встраивается в body
            // Перемещаем его в наш контейнер
            const yandexFrame = document.querySelector('iframe[src*="yandex.ru"]');
            if (yandexFrame && yandexFrame.parentElement) {
                container.appendChild(yandexFrame);
            }
        }
    } catch (error) {
        console.error('Failed to initialize Yandex ID widget:', error);
        throw error;
    }
};

/**
 * Инициализация кнопки Yandex ID (альтернативный вариант)
 */
export const initYandexIDButton = async (
    containerId: string,
    config: YandexIDConfig
): Promise<void> => {
    if (!window.YaAuthSuggest) {
        console.error('YaAuthSuggest is not loaded');
        throw new Error('YaAuthSuggest SDK is not loaded');
    }

    try {
        // Инициализируем кнопку
        const result = await window.YaAuthSuggest.init(
            {
                client_id: config.clientId,
                response_type: 'token',
                redirect_uri: config.redirectUri,
            },
            window.location.origin,
            {
                view: 'button',
                parentId: containerId,
                buttonView: 'main',
                buttonTheme: 'light',
                buttonSize: 'l',
                buttonBorderRadius: 12,
            }
        );

        if (result.status === 'error') {
            console.error('YaAuthSuggest init error:', result.code);
            throw new Error(`YaAuthSuggest init failed: ${result.code}`);
        }

        // Вызываем handler для отображения кнопки
        if (result.handler) {
            await result.handler();
            console.log('Yandex ID button rendered successfully');
        }
    } catch (error) {
        console.error('Failed to initialize Yandex ID button:', error);
        throw error;
    }
};

/**
 * Создание URL для OAuth авторизации Yandex
 */
export const createYandexOAuthUrl = (config: YandexIDConfig): string => {
    const params = new URLSearchParams({
        response_type: 'token',
        client_id: config.clientId,
        redirect_uri: config.redirectUri,
    });

    return `https://oauth.yandex.ru/authorize?${params.toString()}`;
};

/**
 * Парсинг токена из URL после редиректа
 */
export const parseTokenFromUrl = (): string | null => {
    const hash = window.location.hash.substring(1);
    const params = new URLSearchParams(hash);
    return params.get('access_token');
};

/**
 * Очистка токена из URL
 */
export const clearTokenFromUrl = (): void => {
    if (window.location.hash) {
        // Очищаем hash без перезагрузки страницы
        window.history.replaceState(
            null,
            '',
            window.location.pathname + window.location.search
        );
    }
};
