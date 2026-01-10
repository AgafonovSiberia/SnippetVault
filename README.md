# SnippetVault

Современное приложение для хранения и организации сниппетов кода с поддержкой полнотекстового поиска.

## 🏗️ Архитектура

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Nginx     │─────▶│   Backend   │─────▶│  PostgreSQL │
│  (Reverse   │      │  (FastAPI)  │      │             │
│   Proxy)    │      │             │      │             │
└──────┬──────┘      └─────────────┘      └─────────────┘
       │
       │
       ▼
┌─────────────┐
│  Frontend   │
│   (React/   │
│    Vite)    │
└─────────────┘
```

## 🚀 Быстрый старт

### Development

```bash
# 1. Клонировать репозиторий
git clone <repo-url>
cd SnippetVault

# 2. Настроить окружение
bash scripts/dev-setup.sh

# 3. Запустить все сервисы
docker compose -f docker-compose.yml -f docker-compose.dev.yml up

# 4. Открыть приложение
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Production

```bash
# 1. Создать .env файл
cp .env.example .env
# Отредактировать .env с production настройками

# 2. Запустить
docker compose up -d

# 3. Приложение доступно на http://localhost
```

## 📁 Структура проекта

```
SnippetVault/
├── backend/          # FastAPI backend (Python 3.13)
├── frontend/         # React frontend (Vite)
├── nginx/            # Reverse proxy configuration
├── scripts/          # Utility scripts
└── docker-compose.yml
```

## 🛠️ Технологии

### Backend
- **FastAPI** - современный Python веб-фреймворк
- **SQLAlchemy** - ORM для работы с БД
- **Alembic** - миграции БД
- **Dishka** - Dependency Injection
- **PostgreSQL** - основная БД

### Frontend
- **React** - UI библиотека
- **TypeScript** - типизированный JavaScript
- **Vite** - build tool
- **TanStack Query** - Server state management

### Infrastructure
- **Docker** - контейнеризация
- **Nginx** - reverse proxy
- **PostgreSQL 16** - база данных

## 📝 Доступные команды

### Development

```bash
# Запустить все сервисы
docker compose -f docker-compose.yml -f docker-compose.dev.yml up

# Запустить только backend
docker compose -f docker-compose.yml -f docker-compose.dev.yml up backend

# Запустить только web
docker compose -f docker-compose.yml -f docker-compose.dev.yml up web

# Пересобрать контейнеры
docker compose -f docker-compose.yml -f docker-compose.dev.yml build

# Остановить все
docker compose -f docker-compose.yml -f docker-compose.dev.yml down

# Остановить и удалить volumes
docker compose -f docker-compose.yml -f docker-compose.dev.yml down -v
```

### Database

```bash
# Создать новую миграцию
docker compose -f docker-compose.yml -f docker-compose.dev.yml exec backend alembic revision --autogenerate -m "description"

# Применить миграции
docker compose -f docker-compose.yml -f docker-compose.dev.yml exec backend alembic upgrade head

# Откатить миграцию
docker compose -f docker-compose.yml -f docker-compose.dev.yml exec backend alembic downgrade -1

# Подключиться к БД
docker compose -f docker-compose.yml -f docker-compose.dev.yml exec postgres psql -U postgres -d snippetvault
```

### Тестирование

```bash
# Backend тесты
docker compose -f docker-compose.yml -f docker-compose.dev.yml exec backend pytest

# Frontend тесты
docker compose -f docker-compose.yml -f docker-compose.dev.yml exec web npm test
```

## 🔐 Аутентификация

Приложение использует Yandex ID Suggest для мгновенной авторизации:

1. Зарегистрируйте приложение на https://oauth.yandex.ru/
2. Добавьте Client ID и Secret в `.env` файлы
3. Укажите Redirect URI: `http://localhost:5173/auth/callback`

## 📚 Документация

- [Backend README](backend/README.md) - подробная документация по backend
- [API Documentation](http://localhost:8000/docs) - Swagger UI (когда сервер запущен)
- [Architecture](backend/ARCHITECTURE.md) - архитектурная документация

## 🤝 Разработка

### Добавление новой функциональности

1. Backend:
   - Создать модели в `backend/app/infrastructure/database/models.py`
   - Создать миграцию: `alembic revision --autogenerate`
   - Реализовать Repository в `infrastructure/repo/`
   - Реализовать Service в `application/`
   - Создать API endpoints в `api/v1/routers/`

2. Frontend:
   - Создать компоненты в `frontend/src/components/`
   - Создать страницы в `frontend/src/pages/`
   - Добавить API клиент в `frontend/src/services/`

### Code Style

- **Backend**: следует PEP8, используется Ruff для форматирования
- **Frontend**: ESLint + Prettier
- **Commits**: следуем Conventional Commits

## 📄 Лицензия

MIT

## 👥 Авторы

Your Team
