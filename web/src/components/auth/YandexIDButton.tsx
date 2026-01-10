import React, { useEffect, useRef, useState } from 'react';
import { Box, Button, CircularProgress, Alert } from '@mui/material';
import {
    loadYandexIDSDK,
    initYandexIDWidget,
    parseTokenFromUrl,
    clearTokenFromUrl,
    createYandexOAuthUrl
} from '../../utils/yandex-id';

/**
 * Yandex ID Button Component
 * Компонент виджета авторизации через Yandex ID
 * 
 * Пробует использовать виджет Мгновенный вход, если не получается - показывает кнопку
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
    const containerRef = useRef<HTMLDivElement>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [showButton, setShowButton] = useState(false);
    const initAttempted = useRef(false);

    useEffect(() => {
        // Проверяем, есть ли токен в URL (после редиректа)
        const token = parseTokenFromUrl();
        if (token) {
            clearTokenFromUrl();
            onSuccess(token);
            return;
        }

        if (initAttempted.current) {
            return;
        }
        initAttempted.current = true;

        // Загружаем и инициализируем Yandex ID SDK
        const initSDK = async () => {
            try {
                // Загружаем SDK
                await loadYandexIDSDK({
                    onload: () => {
                        console.log('Yandex ID SDK loaded successfully');
                    },
                });

                // Ждем небольшую задержку для полной инициализации
                await new Promise(resolve => setTimeout(resolve, 200));

                try {
                    // Пробуем виджет Мгновенный вход
                    await initYandexIDWidget('yandex-id-container', {
                        clientId,
                        redirectUri,
                    });

                    // Проверяем через 500мс, отрисовался ли виджет
                    setTimeout(() => {
                        const container = document.getElementById('yandex-id-container');
                        const hasContent = container &&
                            (container.querySelector('iframe') ||
                                container.querySelector('button') ||
                                (container.innerHTML.trim().length > 100));

                        if (!hasContent) {
                            console.log('Suggest widget is empty, showing button fallback');
                            setShowButton(true);
                        }
                        setIsLoading(false);
                    }, 500);
                } catch (widgetError) {
                    // Если виджет не сработал, пробуем кнопку
                    console.warn('Widget failed, trying button:', widgetError);
                    setShowButton(true);
                    setIsLoading(false);
                }
            } catch (err) {
                console.error('Failed to initialize Yandex ID:', err);
                setError('Не удалось загрузить виджет авторизации');
                setShowButton(true);
                setIsLoading(false);

                if (onError && err instanceof Error) {
                    onError(err);
                }
            }
        };

        initSDK();
    }, [clientId, redirectUri, onSuccess, onError]);

    /**
     * Обработчик клика по кнопке - открываем OAuth
     */
    const handleButtonClick = () => {
        const oauthUrl = createYandexOAuthUrl({ clientId, redirectUri });
        window.location.href = oauthUrl;
    };

    // Показываем fallback при ошибке
    if (error) {
        return (
            <Box>
                <Alert severity="warning" sx={{ mb: 2 }}>
                    {error}
                </Alert>
                <Button
                    variant="contained"
                    fullWidth
                    size="large"
                    onClick={handleButtonClick}
                    sx={{
                        backgroundColor: '#ffcc00',
                        color: '#000',
                        fontWeight: 600,
                        '&:hover': {
                            backgroundColor: '#e6b800',
                        },
                    }}
                >
                    Войти через Яндекс ID
                </Button>
            </Box>
        );
    }

    return (
        <Box sx={{ width: '100%', position: 'relative', minHeight: '60px' }}>
            {/* Loading overlay */}
            {isLoading && (
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
                        width: '100%',
                        zIndex: 1,
                        backgroundColor: 'rgba(0,0,0,0.02)',
                    }}
                >
                    <CircularProgress size={32} />
                </Box>
            )}

            {/* Yandex ID widget container - всегда в DOM */}
            {!showButton && (
                <Box
                    id="yandex-id-container"
                    ref={containerRef}
                    sx={{
                        width: '100%',
                        minHeight: '60px',
                        display: 'flex',
                        justifyContent: 'center',
                        alignItems: 'center',
                        opacity: isLoading ? 0 : 1,
                        transition: 'opacity 0.3s ease',
                    }}
                />
            )}

            {/* Fallback button - показывается если виджет пустой */}
            {showButton && !isLoading && (
                <Button
                    variant="contained"
                    fullWidth
                    size="large"
                    onClick={handleButtonClick}
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
