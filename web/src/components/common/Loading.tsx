import React from 'react';
import { Box, CircularProgress, Typography } from '@mui/material';

/**
 * Loading Component
 * Компонент загрузки с кастомизируемым сообщением
 */

interface LoadingProps {
    message?: string;
    size?: number;
}

export const Loading: React.FC<LoadingProps> = ({
    message = 'Загрузка...',
    size = 40
}) => {
    return (
        <Box
            sx={{
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center',
                alignItems: 'center',
                minHeight: '200px',
                gap: 2,
            }}
        >
            <CircularProgress size={size} />
            {message && (
                <Typography variant="body1" color="text.secondary">
                    {message}
                </Typography>
            )}
        </Box>
    );
};

export default Loading;
