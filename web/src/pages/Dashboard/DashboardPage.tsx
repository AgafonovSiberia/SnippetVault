import React from 'react';
import {
    Box,
    Container,
    Typography,
    Paper,
    AppBar,
    Toolbar,
    Avatar,
    IconButton,
    Menu,
    MenuItem,
} from '@mui/material';
import { Logout as LogoutIcon } from '@mui/icons-material';
import { useAuth } from '../../hooks/useAuth';
import { useNavigate } from 'react-router-dom';
import { Loading } from '../../components/common';

/**
 * Dashboard Page Component
 * Главная страница приложения после авторизации
 */

export const DashboardPage: React.FC = () => {
    const { user, logout, isLoading } = useAuth();
    const navigate = useNavigate();
    const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);

    const handleMenu = (event: React.MouseEvent<HTMLElement>) => {
        setAnchorEl(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
    };

    const handleLogout = async () => {
        await logout();
        navigate('/');
    };

    if (isLoading) {
        return <Loading message="Загрузка..." />;
    }

    return (
        <Box sx={{ flexGrow: 1 }}>
            {/* AppBar */}
            <AppBar position="static" elevation={0}>
                <Toolbar>
                    <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                        SnippetVault
                    </Typography>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                        <Typography variant="body2">
                            {user?.display_name || 'Пользователь'}
                        </Typography>
                        <IconButton
                            size="large"
                            aria-label="account of current user"
                            aria-controls="menu-appbar"
                            aria-haspopup="true"
                            onClick={handleMenu}
                            color="inherit"
                        >
                            <Avatar
                                src={user?.avatar_url || undefined}
                                alt={user?.display_name || 'User'}
                                sx={{ width: 32, height: 32 }}
                            />
                        </IconButton>
                        <Menu
                            id="menu-appbar"
                            anchorEl={anchorEl}
                            anchorOrigin={{
                                vertical: 'top',
                                horizontal: 'right',
                            }}
                            keepMounted
                            transformOrigin={{
                                vertical: 'top',
                                horizontal: 'right',
                            }}
                            open={Boolean(anchorEl)}
                            onClose={handleClose}
                        >
                            <MenuItem onClick={handleLogout}>
                                <LogoutIcon sx={{ mr: 1 }} />
                                Выйти
                            </MenuItem>
                        </Menu>
                    </Box>
                </Toolbar>
            </AppBar>

            {/* Main Content */}
            <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
                <Paper
                    sx={{
                        p: 4,
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                        minHeight: '400px',
                        justifyContent: 'center',
                    }}
                >
                    <Typography variant="h4" gutterBottom>
                        Добро пожаловать в SnippetVault!
                    </Typography>
                    <Typography variant="body1" color="text.secondary" align="center" sx={{ mb: 3 }}>
                        Здесь скоро появится функционал для управления сниппетами
                    </Typography>
                    <Box sx={{ mt: 2 }}>
                        <Typography variant="body2" color="text.secondary">
                            ID пользователя: {user?.id}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                            Дата регистрации: {user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}
                        </Typography>
                    </Box>
                </Paper>
            </Container>
        </Box>
    );
};

export default DashboardPage;
