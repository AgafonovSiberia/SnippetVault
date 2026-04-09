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
import { SimpleYandexButton } from '../../components/auth/SimpleYandexButton';
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


    return (
        <Box
            sx={{
                minHeight: '100vh',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                background: `radial-gradient(ellipse at top, ${alpha(theme.palette.primary.dark, 0.25)} 0%, ${theme.palette.background.default} 50%), radial-gradient(ellipse at bottom, ${alpha(theme.palette.secondary.dark, 0.2)} 0%, ${theme.palette.background.default} 50%)`,
                position: 'relative',
                overflow: 'hidden',
                '&::before': {
                    content: '""',
                    position: 'absolute',
                    top: '10%',
                    right: '15%',
                    width: '500px',
                    height: '500px',
                    borderRadius: '50%',
                    background: `radial-gradient(circle, ${alpha(theme.palette.primary.main, 0.25)} 0%, transparent 70%)`,
                    filter: 'blur(100px)',
                    animation: 'float 8s ease-in-out infinite',
                },
                '&::after': {
                    content: '""',
                    position: 'absolute',
                    bottom: '15%',
                    left: '10%',
                    width: '400px',
                    height: '400px',
                    borderRadius: '50%',
                    background: `radial-gradient(circle, ${alpha(theme.palette.info.main, 0.2)} 0%, transparent 70%)`,
                    filter: 'blur(100px)',
                    animation: 'float 10s ease-in-out infinite reverse',
                },
                '@keyframes float': {
                    '0%, 100%': {
                        transform: 'translate(0, 0)',
                    },
                    '50%': {
                        transform: 'translate(30px, -30px)',
                    },
                },
            }}
        >
            <Container maxWidth="sm">
                <Paper
                    elevation={0}
                    sx={{
                        p: { xs: 4, sm: 6 },
                        borderRadius: 3,
                        backdropFilter: 'blur(40px)',
                        backgroundColor: alpha(theme.palette.background.paper, 0.85),
                        border: `1px solid ${alpha(theme.palette.primary.main, 0.3)}`,
                        position: 'relative',
                        zIndex: 1,
                        boxShadow: `0 20px 60px ${alpha(theme.palette.common.black, 0.5)}`,
                        background: `linear-gradient(135deg, ${alpha(theme.palette.background.paper, 0.9)} 0%, ${alpha(theme.palette.background.paper, 0.8)} 100%)`,
                    }}
                >
                    <Stack spacing={4} alignItems="center">
                        {/* Logo and Title */}
                        <Box
                            sx={{
                                display: 'flex',
                                alignItems: 'center',
                                gap: 2,
                                mb: 1,
                            }}
                        >
                            <Box
                                sx={{
                                    width: 56,
                                    height: 56,
                                    borderRadius: 2.5,
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    background: `linear-gradient(135deg, ${theme.palette.primary.main} 0%, ${theme.palette.secondary.main} 100%)`,
                                    boxShadow: `0 8px 24px ${alpha(theme.palette.primary.main, 0.5)}`,
                                    animation: 'glow 3s ease-in-out infinite',
                                    '@keyframes glow': {
                                        '0%, 100%': {
                                            boxShadow: `0 8px 24px ${alpha(theme.palette.primary.main, 0.5)}`,
                                        },
                                        '50%': {
                                            boxShadow: `0 8px 32px ${alpha(theme.palette.primary.main, 0.8)}`,
                                        },
                                    },
                                }}
                            >
                                <CodeIcon sx={{ fontSize: 32, color: 'white' }} />
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
                            <Typography
                                variant="h5"
                                gutterBottom
                                fontWeight={600}
                                sx={{ color: 'text.primary' }}
                            >
                                Добро пожаловать!
                            </Typography>
                            <Typography
                                variant="body1"
                                color="text.secondary"
                                sx={{ fontSize: '0.95rem' }}
                            >
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
                                    backgroundColor: alpha(theme.palette.error.main, 0.1),
                                    border: `1px solid ${alpha(theme.palette.error.main, 0.3)}`,
                                }}
                            >
                                {error}
                            </Alert>
                        )}

                        {/* Yandex ID Button */}
                        <Box sx={{ width: '100%', maxWidth: '320px' }}>
                            <SimpleYandexButton
                                onSuccess={handleSuccess}
                                clientId={YANDEX_CLIENT_ID}
                                redirectUri={YANDEX_REDIRECT_URI}
                            />
                        </Box>

                        {/* Additional Info */}
                        <Box sx={{ textAlign: 'center', pt: 1 }}>
                            <Typography
                                variant="caption"
                                color="text.secondary"
                                sx={{ fontSize: '0.8rem' }}
                            >
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
