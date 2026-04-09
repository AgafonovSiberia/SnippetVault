import React, { useEffect, useState } from 'react';
import { Box, CircularProgress, Alert, Button } from '@mui/material';
import {
    parseTokenFromUrl,
    clearTokenFromUrl,
    createYandexOAuthUrl
} from '../../utils/yandex-id';

/**
 * Simplified Yandex ID Button Component using direct iframe approach
 * 
 * Стратегия:
 * 1. Создаем контейнер для виджета
 * 2. Загружаем Yandex SDK
 * 3. Инициализируем виджет с view='button'
 * 4. Если не работает - показываем fallback кнопку
 */

interface YandexIDButtonProps {
    onSuccess: (token: string) => void;
    onError?: (error: Error) => void;
    clientId: string;
    redirectUri: string;
}

export const YandexIDButton: React.FC<YandexIDButtonProps> = ({
    onSuccess,
    onError,
    clientId,
    redirectUri,
}) => {
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [useFallback, setUseFallback] = useState(false);

    useEffect(() => {
        // Проверяем токен в URL (после редиректа)
        const token = parseTokenFromUrl();
        if (token) {
            clearTokenFromUrl();
            onSuccess(token);
            return;
        }

        // Загружаем SDK
        const loadSDK = async () => {
            try {
                // Проверяем, загружен ли уже SDK
                if (window.YaAuthSuggest) {
                    console.log('Yandex SDK already loaded');
                    initWidget();
                    return;
                }

                // Загружаем SDK
                const script = document.createElement('script');
                script.src = 'https://yastatic.net/s3/passport-sdk/autofill/v1/sdk-suggest-with-polyfills-latest.js';
                script.async = true;
                script.onload = () => {
                    console.log('Yandex SDK loaded');
                    // Даем SDK время на инициализацию
                    setTimeout(initWidget, 200);
                };
                script.onerror = () => {
                    console.error('Failed to load Yandex SDK');
                    setUseFallback(true);
                    setIsLoading(false);
                };
                document.head.appendChild(script);
            } catch (err) {
                console.error('SDK load error:', err);
                setUseFallback(true);
                setIsLoading(false);
            }
        };

        // Инициализируем виджет
        const initWidget = async () => {
            if (!window.YaAuthSuggest) {
                console.error('YaAuthSuggest not available');
                setUseFallback(true);
                setIsLoading(false);
                return;
            }

            try {
                console.log('Initializing Yandex widget with Button view...');

                const result = await window.YaAuthSuggest.init(
                    {
                        client_id: clientId,
                        response_type: 'token',
                        redirect_uri: redirectUri,
                    },
                    window.location.origin,
                    {
                        view: 'button',
                        parentId: 'yandex-widget-container',
                        buttonView: 'main',
                        buttonTheme: 'light',
                        buttonSize: 'l',
                        buttonBorderRadius: 12,
                    }
                );

                console.log('Widget init result:', result);

                if (result.status === 'error') {
                    console.warn('Widget returned error:', result.code);
                    // Даже если статус error, пробуем вызвать handler
                    // Он может отрисовать кнопку
                    if (result.handler) {
                        try {
                            await result.handler();
                            console.log('Handler executed despite error status');
                        } catch (handlerError) {
                            console.error('Handler error:', handlerError);
                        }
                    }

                    // Проверяем через 1 секунду, отрисовалось ли что-то
                    setTimeout(() => {
                        const container = document.getElementById('yandex-widget-container');
                        const hasContent = container && container.children.length > 0;

                        if (hasContent) {
                            console.log('Widget rendered despite error status');
                            setIsLoading(false);
                        } else {
                            console.log('No widget content, using fallback');
                            setUseFallback(true);
                            setIsLoading(false);
                        }
                    }, 1000);
                    return;
                }

                // Вызываем handler для отрисовки
                if (result.handler) {
                    await result.handler();
                    console.log('Widget handler called successfully');
                }

                // Ждем отрисовки
                setTimeout(() => {
                    const container = document.getElementById('yandex-widget-container');
                    const hasContent = container && container.children.length > 0;

                    if (hasContent) {
                        console.log('Widget rendered successfully');
                        setIsLoading(false);
                    } else {
                        console.log('Widget container is empty, using fallback');
                        setUseFallback(true);
                        setIsLoading(false);
                    }
                }, 1000);

            } catch (err) {
                console.error('Widget init error:', err);
                setError('Ошибка инициализации виджета');
                setUseFallback(true);
                setIsLoading(false);

                if (onError && err instanceof Error) {
                    onError(err);
                }
            }
        };

        loadSDK();
    }, [clientId, redirectUri, onSuccess, onError]);

    const handleFallbackClick = () => {
        const oauthUrl = createYandexOAuthUrl({ clientId, redirectUri });
        window.location.href = oauthUrl;
    };

    return (
        <Box sx={{ width: '100%', position: 'relative', minHeight: '60px' }}>
            {/* Yandex Widget Container - всегда в DOM */}
            <Box
                id="yandex-widget-container"
                sx={{
                    width: '100%',
                    minHeight: '60px',
                    display: useFallback ? 'none' : 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                    opacity: isLoading ? 0 : 1,
                    transition: 'opacity 0.3s ease',
                }}
            />

            {/* Loading Spinner */}
            {isLoading && !useFallback && (
                <Box
                    sx={{
                        position: 'absolute',
                        top: 0,
                        left: 0,
                        right: 0,
                        bottom: 0,
                        display: 'flex',
                        justifyContent: 'center',
                        alignItems: 'center',
                        minHeight: '60px',
                    }}
                >
                    <CircularProgress size={32} />
                </Box>
            )}

            {/* Error Alert */}
            {error && (
                <Alert severity="warning" sx={{ mb: 2 }}>
                    {error}
                </Alert>
            )}

            {/* Fallback Button */}
            {useFallback && (
                <Button
                    variant="contained"
                    fullWidth
                    size="large"
                    onClick={handleFallbackClick}
                    sx={{
                        backgroundColor: '#ffcc00',
                        color: '#000',
                        fontWeight: 600,
                        py: 1.5,
                        fontSize: '1rem',
                        '&:hover': {
                            backgroundColor: '#e6b800',
                            transform: 'translateY(-2px)',
                        },
                        transition: 'all 0.2s ease',
                    }}
                >
                    Войти через Яндекс ID
                </Button>
            )}
        </Box>
    );
};

export default YandexIDButton;
