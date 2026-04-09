import { createTheme } from '@mui/material/styles';

/**
 * Material UI Theme Configuration
 * Настройка темы приложения с использованием Material Design 3
 */

export const theme = createTheme({
    palette: {
        mode: 'dark',
        primary: {
            main: '#8b5cf6', // Фиолетовый как на референсе
            light: '#a78bfa',
            dark: '#7c3aed',
            contrastText: '#fff',
        },
        secondary: {
            main: '#a78bfa', // Светло-фиолетовый
            light: '#c4b5fd',
            dark: '#8b5cf6',
            contrastText: '#fff',
        },
        background: {
            default: '#1a1a2e', // Темно-синий вместо черного
            paper: '#252545', // Темно-фиолетовый серый для карточек
        },
        text: {
            primary: '#f0f0f0',
            secondary: '#a8a8b8', // Более светлый серый текст
        },
        error: {
            main: '#ef4444',
        },
        warning: {
            main: '#f59e0b',
        },
        info: {
            main: '#60a5fa', // Синий как на референсе
        },
        success: {
            main: '#10b981',
        },
    },
    typography: {
        fontFamily: [
            'Inter',
            '-apple-system',
            'BlinkMacSystemFont',
            '"Segoe UI"',
            'Roboto',
            '"Helvetica Neue"',
            'Arial',
            'sans-serif',
        ].join(','),
        h1: {
            fontSize: '3rem',
            fontWeight: 700,
            lineHeight: 1.2,
        },
        h2: {
            fontSize: '2.5rem',
            fontWeight: 700,
            lineHeight: 1.3,
        },
        h3: {
            fontSize: '2rem',
            fontWeight: 600,
            lineHeight: 1.4,
        },
        h4: {
            fontSize: '1.5rem',
            fontWeight: 600,
            lineHeight: 1.4,
        },
        h5: {
            fontSize: '1.25rem',
            fontWeight: 600,
            lineHeight: 1.5,
        },
        h6: {
            fontSize: '1rem',
            fontWeight: 600,
            lineHeight: 1.5,
        },
        button: {
            textTransform: 'none',
            fontWeight: 500,
        },
    },
    shape: {
        borderRadius: 12,
    },
    components: {
        MuiButton: {
            styleOverrides: {
                root: {
                    borderRadius: 12,
                    padding: '10px 24px',
                    fontSize: '1rem',
                    fontWeight: 500,
                    transition: 'all 0.3s ease',
                    '&:hover': {
                        transform: 'translateY(-2px)',
                        boxShadow: '0 8px 16px rgba(0,0,0,0.2)',
                    },
                },
                contained: {
                    boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
                },
            },
        },
        MuiCard: {
            styleOverrides: {
                root: {
                    borderRadius: 16,
                    boxShadow: '0 8px 32px rgba(0,0,0,0.1)',
                    transition: 'all 0.3s ease',
                    '&:hover': {
                        boxShadow: '0 12px 48px rgba(0,0,0,0.15)',
                    },
                },
            },
        },
        MuiTextField: {
            styleOverrides: {
                root: {
                    '& .MuiOutlinedInput-root': {
                        borderRadius: 12,
                    },
                },
            },
        },
        MuiPaper: {
            styleOverrides: {
                root: {
                    borderRadius: 16,
                },
            },
        },
    },
});

export default theme;
