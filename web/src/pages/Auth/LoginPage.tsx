import React, { useState } from 'react';
import {
    Box,
    Container,
    Paper,
    Typography,
    Alert,
    Stack,
    useTheme,
    alpha,
} from '@mui/material';
import { Code as CodeIcon } from '@mui/icons-material';
import { YandexIDButton } from '../../components/auth';
import { useAuth } from '../../hooks/useAuth';
import { useNavigate } from 'react-router-dom';

/**
 * Login Page Component
 * Страница авторизации с использованием Yandex ID
 */

const YANDEX_CLIENT_ID = import.meta.env.VITE_YANDEX_CLIENT_ID || 'your_yandex_client_id';
const YANDEX_REDIRECT_URI = import.meta.env.VITE_YANDEX_REDIRECT_URI || `${window.location.origin}/`;

export const LoginPage: React.FC = () => {
    const theme = useTheme();
    const navigate = useNavigate();
    const { login } = useAuth();
    const [error, setError] = useState<string | null>(null);

    const handleSuccess = async (token: string) => {
        setError(null);

        try {
            await login(token);
            navigate('/dashboard'); // Перенаправляем на дашборд после успешной авторизации
        } catch (err) {
            console.error('Login failed:', err);
            setError('Не удалось выполнить вход. Пожалуйста, попробуйте еще раз.');
        }
    };

    const handleError = (err: Error) => {
        console.error('Yandex ID error:', err);
        setError('Ошибка при загрузке виджета авторизации');
    };

    return (
        <Box
            sx={{
                minHeight: '100vh',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                background: `linear-gradient(135deg, ${alpha(theme.palette.primary.main, 0.1)} 0%, ${alpha(theme.palette.secondary.main, 0.1)} 100%)`,
                position: 'relative',
                overflow: 'hidden',
                '&::before': {
                    content: '""',
                    position: 'absolute',
                    top: '-10%',
                    right: '-10%',
                    width: '40%',
                    height: '40%',
                    borderRadius: '50%',
                    background: `radial-gradient(circle, ${alpha(theme.palette.primary.main, 0.2)} 0%, transparent 70%)`,
                    filter: 'blur(80px)',
                },
                '&::after': {
                    content: '""',
                    position: 'absolute',
                    bottom: '-10%',
                    left: '-10%',
                    width: '40%',
                    height: '40%',
                    borderRadius: '50%',
                    background: `radial-gradient(circle, ${alpha(theme.palette.secondary.main, 0.2)} 0%, transparent 70%)`,
                    filter: 'blur(80px)',
                },
            }}
        >
            <Container maxWidth="sm">
                <Paper
                    elevation={0}
                    sx={{
                        p: { xs: 3, sm: 5 },
                        borderRadius: 4,
                        backdropFilter: 'blur(20px)',
                        backgroundColor: alpha(theme.palette.background.paper, 0.8),
                        border: `1px solid ${alpha(theme.palette.primary.main, 0.1)}`,
                        position: 'relative',
                        zIndex: 1,
                        boxShadow: `0 8px 32px ${alpha(theme.palette.common.black, 0.2)}`,
                    }}
                >
                    <Stack spacing={4} alignItems="center">
                        {/* Logo and Title */}
                        <Box
                            sx={{
                                display: 'flex',
                                alignItems: 'center',
                                gap: 2,
                                mb: 2,
                            }}
                        >
                            <Box
                                sx={{
                                    width: 64,
                                    height: 64,
                                    borderRadius: 3,
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    background: `linear-gradient(135deg, ${theme.palette.primary.main} 0%, ${theme.palette.secondary.main} 100%)`,
                                    boxShadow: `0 4px 20px ${alpha(theme.palette.primary.main, 0.4)}`,
                                    animation: 'pulse 2s ease-in-out infinite',
                                    '@keyframes pulse': {
                                        '0%, 100%': {
                                            transform: 'scale(1)',
                                        },
                                        '50%': {
                                            transform: 'scale(1.05)',
                                        },
                                    },
                                }}
                            >
                                <CodeIcon sx={{ fontSize: 36, color: 'white' }} />
                            </Box>
                            <Typography
                                variant="h3"
                                component="h1"
                                sx={{
                                    fontWeight: 700,
                                    background: `linear-gradient(135deg, ${theme.palette.primary.main} 0%, ${theme.palette.secondary.main} 100%)`,
                                    WebkitBackgroundClip: 'text',
                                    WebkitTextFillColor: 'transparent',
                                    backgroundClip: 'text',
                                }}
                            >
                                SnippetVault
                            </Typography>
                        </Box>

                        {/* Welcome Text */}
                        <Box sx={{ textAlign: 'center' }}>
                            <Typography variant="h5" gutterBottom fontWeight={600}>
                                Добро пожаловать!
                            </Typography>
                            <Typography variant="body1" color="text.secondary">
                                Сохраняйте, организуйте и находите ваши сниппеты кода
                            </Typography>
                        </Box>

                        {/* Error Alert */}
                        {error && (
                            <Alert
                                severity="error"
                                sx={{
                                    width: '100%',
                                    borderRadius: 2,
                                }}
                            >
                                {error}
                            </Alert>
                        )}

                        {/* Yandex ID Button */}
                        <Box sx={{ width: '60%' }}>
                            <YandexIDButton
                                onSuccess={handleSuccess}
                                onError={handleError}
                                clientId={YANDEX_CLIENT_ID}
                                redirectUri={YANDEX_REDIRECT_URI}
                            />
                        </Box>

                        {/* Additional Info */}
                        <Box sx={{ textAlign: 'center', pt: 2 }}>
                            <Typography variant="caption" color="text.secondary">
                                Используя сервис, вы соглашаетесь с условиями использования
                            </Typography>
                        </Box>
                    </Stack>
                </Paper>
            </Container>
        </Box>
    );
};

export default LoginPage;
