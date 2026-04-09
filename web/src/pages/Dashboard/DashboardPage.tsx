import React, { useState, useEffect } from 'react';
import {
    Box,
    Typography,
    AppBar,
    Toolbar,
    Avatar,
    IconButton,
    Menu,
    MenuItem,
    alpha,
    useTheme,
    Snackbar,
    Alert,
} from '@mui/material';
import { Logout as LogoutIcon, Search as SearchIcon } from '@mui/icons-material';
import { useAuth } from '../../hooks/useAuth';
import { useNavigate } from 'react-router-dom';
import { Loading } from '../../components/common';
import {
    Sidebar,
    FolderCard,
    SnippetCard,
    SnippetViewer,
    ProjectDialog,
    FolderDialog,
    SnippetDialog,
    DeleteConfirmDialog,
} from '../../components/dashboard';
import { snippetsService } from '../../services';
import type { Project, Folder, Snippet } from '../../types';

/**
 * Dashboard Page Component
 * Главная страница приложения после авторизации
 */

export const DashboardPage: React.FC = () => {
    const { user, logout, isLoading: authLoading } = useAuth();
    const navigate = useNavigate();
    const theme = useTheme();

    // UI State
    const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
    const [selectedId, setSelectedId] = useState<string>('overview');
    const [selectedType, setSelectedType] = useState<'project' | 'folder' | 'snippet'>('project');

    // Data State
    const [projects, setProjects] = useState<Project[]>([]);
    const [folders, setFolders] = useState<Folder[]>([]);
    const [snippets, setSnippets] = useState<Snippet[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    // Dialog State
    const [projectDialog, setProjectDialog] = useState<{ open: boolean; project?: Project | null }>({ open: false });
    const [folderDialog, setFolderDialog] = useState<{ open: boolean; folder?: Folder | null; projectId?: string }>({ open: false });
    const [snippetDialog, setSnippetDialog] = useState<{ open: boolean; snippet?: Snippet | null; projectId?: string; folderId?: string }>({ open: false });
    const [deleteDialog, setDeleteDialog] = useState<{ open: boolean; type?: string; id?: string; name?: string }>({ open: false });

    // Snackbar State
    const [snackbar, setSnackbar] = useState<{ open: boolean; message: string; severity: 'success' | 'error' }>({
        open: false,
        message: '',
        severity: 'success',
    });

    // Load initial data
    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        try {
            setIsLoading(true);
            const [projectsData, foldersData, snippetsData] = await Promise.all([
                snippetsService.getProjects(),
                snippetsService.getFolders(),
                snippetsService.getSnippets(),
            ]);
            setProjects(projectsData);
            setFolders(foldersData);
            setSnippets(snippetsData);
        } catch (error) {
            console.error('Failed to load data:', error);
            showSnackbar('Ошибка загрузки данных', 'error');
        } finally {
            setIsLoading(false);
        }
    };

    const showSnackbar = (message: string, severity: 'success' | 'error' = 'success') => {
        setSnackbar({ open: true, message, severity });
    };

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

    const handleSelect = (id: string, type: 'project' | 'folder' | 'snippet') => {
        setSelectedId(id);
        setSelectedType(type);
    };

    // Project CRUD
    const handleCreateProject = () => {
        setProjectDialog({ open: true, project: null });
    };

    const handleEditProject = (project: Project) => {
        setProjectDialog({ open: true, project });
    };

    const handleSaveProject = async (data: { name: string; description?: string }) => {
        try {
            if (projectDialog.project) {
                await snippetsService.updateProject(projectDialog.project.id, data);
                showSnackbar('Проект обновлен');
            } else {
                await snippetsService.createProject(data);
                showSnackbar('Проект создан');
            }
            loadData();
        } catch (error) {
            console.error('Failed to save project:', error);
            showSnackbar('Ошибка сохранения проекта', 'error');
        }
    };

    const handleDeleteProject = async (id: string) => {
        try {
            await snippetsService.deleteProject(id);
            showSnackbar('Проект удален');
            if (selectedId === id) {
                setSelectedId('overview');
                setSelectedType('project');
            }
            loadData();
        } catch (error) {
            console.error('Failed to delete project:', error);
            showSnackbar('Ошибка удаления проекта', 'error');
        }
    };

    // Folder CRUD
    const handleCreateFolder = (projectId: string) => {
        setFolderDialog({ open: true, folder: null, projectId });
    };

    const handleEditFolder = (folder: Folder) => {
        setFolderDialog({ open: true, folder, projectId: folder.project_id });
    };

    const handleSaveFolder = async (data: { name: string; description?: string; project_id: string }) => {
        try {
            if (folderDialog.folder) {
                await snippetsService.updateFolder(folderDialog.folder.id, {
                    name: data.name,
                    description: data.description,
                });
                showSnackbar('Папка обновлена');
            } else {
                await snippetsService.createFolder(data);
                showSnackbar('Папка создана');
            }
            loadData();
        } catch (error) {
            console.error('Failed to save folder:', error);
            showSnackbar('Ошибка сохранения папки', 'error');
        }
    };

    const handleDeleteFolder = async (id: string) => {
        try {
            await snippetsService.deleteFolder(id);
            showSnackbar('Папка удалена');
            if (selectedId === id) {
                const folder = folders.find((f) => f.id === id);
                if (folder) {
                    setSelectedId(folder.project_id);
                    setSelectedType('project');
                }
            }
            loadData();
        } catch (error) {
            console.error('Failed to delete folder:', error);
            showSnackbar('Ошибка удаления папки', 'error');
        }
    };

    // Snippet CRUD
    const handleCreateSnippet = (projectId: string, folderId?: string) => {
        setSnippetDialog({ open: true, snippet: null, projectId, folderId });
    };

    const handleEditSnippet = (snippet: Snippet) => {
        setSnippetDialog({
            open: true,
            snippet,
            projectId: snippet.project_id,
            folderId: snippet.folder_id,
        });
    };

    const handleSaveSnippet = async (data: {
        title: string;
        content: string;
        language: string;
        project_id: string;
        folder_id?: string;
        description?: string;
        tags?: string[];
    }) => {
        try {
            if (snippetDialog.snippet) {
                await snippetsService.updateSnippet(snippetDialog.snippet.id, {
                    title: data.title,
                    content: data.content,
                    language: data.language,
                    folder_id: data.folder_id,
                    description: data.description,
                    tags: data.tags,
                });
                showSnackbar('Сниппет обновлен');
            } else {
                await snippetsService.createSnippet(data);
                showSnackbar('Сниппет создан');
            }
            loadData();
        } catch (error) {
            console.error('Failed to save snippet:', error);
            showSnackbar('Ошибка сохранения сниппета', 'error');
        }
    };

    const handleDeleteSnippet = async (id: string) => {
        try {
            await snippetsService.deleteSnippet(id);
            showSnackbar('Сниппет удален');
            const snippet = snippets.find((s) => s.id === id);
            if (selectedId === id && snippet) {
                if (snippet.folder_id) {
                    setSelectedId(snippet.folder_id);
                    setSelectedType('folder');
                } else {
                    setSelectedId(snippet.project_id);
                    setSelectedType('project');
                }
            }
            loadData();
        } catch (error) {
            console.error('Failed to delete snippet:', error);
            showSnackbar('Ошибка удаления сниппета', 'error');
        }
    };

    const handleToggleFavorite = async (id: string) => {
        try {
            await snippetsService.toggleFavorite(id);
            loadData();
        } catch (error) {
            console.error('Failed to toggle favorite:', error);
            showSnackbar('Ошибка изменения избранного', 'error');
        }
    };

    // Delete confirmation
    const handleDeleteClick = (type: string, id: string, name: string) => {
        setDeleteDialog({ open: true, type, id, name });
    };

    const handleConfirmDelete = () => {
        if (!deleteDialog.id || !deleteDialog.type) return;

        switch (deleteDialog.type) {
            case 'project':
                handleDeleteProject(deleteDialog.id);
                break;
            case 'folder':
                handleDeleteFolder(deleteDialog.id);
                break;
            case 'snippet':
                handleDeleteSnippet(deleteDialog.id);
                break;
        }
    };

    // Render main content
    const renderMainContent = () => {
        // Show snippet details
        if (selectedType === 'snippet') {
            const snippet = snippets.find((s) => s.id === selectedId);
            if (snippet) {
                return (
                    <SnippetViewer
                        snippet={snippet}
                        onToggleFavorite={() => handleToggleFavorite(snippet.id)}
                        onEdit={() => handleEditSnippet(snippet)}
                        onDelete={() => handleDeleteClick('snippet', snippet.id, snippet.title)}
                        onCopy={() => {
                            navigator.clipboard.writeText(snippet.content);
                            showSnackbar('Код скопирован');
                        }}
                    />
                );
            }
        }

        // Show project contents (folders and snippets)
        if (selectedType === 'project' && selectedId !== 'overview') {
            const projectFolders = folders.filter((f) => f.project_id === selectedId);
            const projectSnippets = snippets.filter((s) => s.project_id === selectedId && !s.folder_id);
            const project = projects.find((p) => p.id === selectedId);

            return (
                <Box sx={{ p: 3 }}>
                    <Box sx={{ mb: 3 }}>
                        <Typography variant="h4" sx={{ fontWeight: 700 }}>
                            {project?.name || 'Project Contents'}
                        </Typography>
                    </Box>

                    {projectFolders.length > 0 && (
                        <Box sx={{ mb: 4 }}>
                            <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                                Folders
                            </Typography>
                            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
                                {projectFolders.map((folder) => (
                                    <Box key={folder.id} sx={{ flex: '1 1 calc(33.333% - 16px)', minWidth: '280px' }}>
                                        <FolderCard
                                            folder={folder}
                                            onClick={() => handleSelect(folder.id, 'folder')}
                                            onEdit={() => handleEditFolder(folder)}
                                            onDelete={() => handleDeleteClick('folder', folder.id, folder.name)}
                                        />
                                    </Box>
                                ))}
                            </Box>
                        </Box>
                    )}

                    {projectSnippets.length > 0 && (
                        <Box>
                            <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                                Snippets
                            </Typography>
                            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
                                {projectSnippets.map((snippet) => (
                                    <Box key={snippet.id} sx={{ flex: '1 1 calc(33.333% - 16px)', minWidth: '280px' }}>
                                        <SnippetCard
                                            snippet={snippet}
                                            onClick={() => handleSelect(snippet.id, 'snippet')}
                                            onEdit={() => handleEditSnippet(snippet)}
                                            onDelete={() => handleDeleteClick('snippet', snippet.id, snippet.title)}
                                        />
                                    </Box>
                                ))}
                            </Box>
                        </Box>
                    )}
                </Box>
            );
        }

        // Show folder contents (snippets)
        if (selectedType === 'folder') {
            const folderSnippets = snippets.filter((s) => s.folder_id === selectedId);
            const folder = folders.find((f) => f.id === selectedId);

            return (
                <Box sx={{ p: 3 }}>
                    <Box sx={{ mb: 3 }}>
                        <Typography variant="h4" sx={{ mb: 1, fontWeight: 700 }}>
                            {folder?.name}
                        </Typography>
                        {folder?.description && (
                            <Typography variant="body2" color="text.secondary">
                                {folder.description}
                            </Typography>
                        )}
                    </Box>

                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
                        {folderSnippets.map((snippet) => (
                            <Box key={snippet.id} sx={{ flex: '1 1 calc(33.333% - 16px)', minWidth: '280px' }}>
                                <SnippetCard
                                    snippet={snippet}
                                    onClick={() => handleSelect(snippet.id, 'snippet')}
                                    onEdit={() => handleEditSnippet(snippet)}
                                    onDelete={() => handleDeleteClick('snippet', snippet.id, snippet.title)}
                                />
                            </Box>
                        ))}
                    </Box>
                </Box>
            );
        }

        // Overview - show all projects
        return (
            <Box sx={{ p: 3 }}>
                <Typography variant="h4" sx={{ mb: 3, fontWeight: 700 }}>
                    All Projects
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
                    {projects.map((project) => (
                        <Box key={project.id} sx={{ flex: '1 1 calc(33.333% - 16px)', minWidth: '280px' }}>
                            <FolderCard
                                folder={{ ...project, folder_id: undefined } as any}
                                onClick={() => handleSelect(project.id, 'project')}
                                onEdit={() => handleEditProject(project)}
                                onDelete={() => handleDeleteClick('project', project.id, project.name)}
                            />
                        </Box>
                    ))}
                </Box>
            </Box>
        );
    };

    if (authLoading || isLoading) {
        return <Loading message="Загрузка..." />;
    }

    return (
        <Box sx={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
            {/* AppBar */}
            <AppBar
                position="static"
                elevation={0}
                sx={{
                    background: theme.palette.background.default,
                    borderBottom: `1px solid ${alpha(theme.palette.primary.main, 0.1)}`,
                }}
            >
                <Toolbar>
                    <Typography
                        variant="h6"
                        component="div"
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

                    <Box sx={{ flexGrow: 1 }} />

                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                        <IconButton sx={{ color: 'text.secondary' }}>
                            <SearchIcon />
                        </IconButton>
                        <Typography variant="body2" color="text.secondary">
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
                            <Avatar src={user?.avatar_url || undefined} alt={user?.display_name || 'User'} sx={{ width: 32, height: 32 }} />
                        </IconButton>
                        <Menu
                            id="menu-appbar"
                            anchorEl={anchorEl}
                            anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
                            keepMounted
                            transformOrigin={{ vertical: 'top', horizontal: 'right' }}
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

            {/* Main Layout */}
            <Box sx={{ display: 'flex', flex: 1, overflow: 'hidden' }}>
                {/* Sidebar */}
                <Sidebar
                    projects={projects}
                    folders={folders}
                    snippets={snippets}
                    selectedId={selectedId}
                    onSelect={handleSelect}
                    onCreateProject={handleCreateProject}
                    onCreateFolder={handleCreateFolder}
                    onCreateSnippet={handleCreateSnippet}
                    onEditProject={handleEditProject}
                    onEditFolder={handleEditFolder}
                    onEditSnippet={handleEditSnippet}
                    onDeleteProject={handleDeleteProject}
                    onDeleteFolder={handleDeleteFolder}
                    onDeleteSnippet={handleDeleteSnippet}
                    onToggleFavorite={handleToggleFavorite}
                />

                {/* Main Content */}
                <Box
                    sx={{
                        flex: 1,
                        overflow: 'auto',
                        background: `radial-gradient(ellipse at top right, ${alpha(theme.palette.primary.dark, 0.05)} 0%, transparent 50%)`,
                    }}
                >
                    {renderMainContent()}
                </Box>
            </Box>

            {/* Dialogs */}
            <ProjectDialog
                open={projectDialog.open}
                project={projectDialog.project}
                onClose={() => setProjectDialog({ open: false })}
                onSave={handleSaveProject}
            />

            <FolderDialog
                open={folderDialog.open}
                folder={folderDialog.folder}
                projectId={folderDialog.projectId || ''}
                onClose={() => setFolderDialog({ open: false })}
                onSave={handleSaveFolder}
            />

            <SnippetDialog
                open={snippetDialog.open}
                snippet={snippetDialog.snippet}
                projectId={snippetDialog.projectId || ''}
                folderId={snippetDialog.folderId}
                onClose={() => setSnippetDialog({ open: false })}
                onSave={handleSaveSnippet}
            />

            <DeleteConfirmDialog
                open={deleteDialog.open}
                title={`Удалить ${deleteDialog.type === 'project' ? 'проект' : deleteDialog.type === 'folder' ? 'папку' : 'сниппет'}?`}
                message={`Вы уверены, что хотите удалить "${deleteDialog.name}"? Это действие нельзя отменить.`}
                onClose={() => setDeleteDialog({ open: false })}
                onConfirm={handleConfirmDelete}
            />

            {/* Snackbar */}
            <Snackbar
                open={snackbar.open}
                autoHideDuration={4000}
                onClose={() => setSnackbar({ ...snackbar, open: false })}
                anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
            >
                <Alert severity={snackbar.severity} variant="filled" onClose={() => setSnackbar({ ...snackbar, open: false })}>
                    {snackbar.message}
                </Alert>
            </Snackbar>
        </Box>
    );
};

export default DashboardPage;
