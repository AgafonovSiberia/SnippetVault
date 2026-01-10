# SnippetVault Backend

Backend API для приложения SnippetVault - системы хранения и управления сниппетами кода.

## 🚀 Технологический стек

- **Python 3.13**
- **FastAPI** - веб-фреймворк
- **SQLAlchemy 2.0** - ORM с async поддержкой
- **PostgreSQL** - база данных
- **Dishka** - dependency injection
- **Pydantic v2** - валидация данных
- **JWT** - аутентификация
- **httpx** - HTTP клиент для OAuth

## 📋 Возможности

### MVP
- ✅ Авторизация через Yandex OAuth
- ✅ JWT токены (access + refresh)
- ✅ Управление пользователями
- 🚧 CRUD операции для проектов
- 🚧 CRUD операции для сниппетов
- 🚧 Система тегов
- 🚧 Full-text поиск

## 🔧 Установка и запуск

### Предварительные требования

1. Python 3.13
2. PostgreSQL 14+
3. UV (рекомендуется) или pip

### Шаги установки

1. **Клонируйте репозиторий и перейдите в папку backend**

```bash
cd backend
```

2. **Создайте виртуальное окружение и установите зависимости**

```bash
# С использованием UV (рекомендуется)
uv venv
uv pip install -e .

# Или с pip
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
pip install -e .
```

3. **Настройте переменные окружения**

Скопируйте `.env.example` в `.env` и заполните необходимые значения:

```bash
cp .env.example .env
```

Обязательные переменные:
- `DB_POSTGRES_*` - настройки подключения к PostgreSQL
- `SECURE_JWT_SECRET` - секретный ключ для JWT (используйте криптостойкий!)
- `PROVIDER_YANDEX_CLIENT_ID` - ID приложения Yandex OAuth
- `PROVIDER_YANDEX_CLIENT_SECRET` - Secret приложения Yandex OAuth

4. **Создайте базу данных**

```bash
createdb snippetvault
```

5. **Примените миграции** (когда будут созданы)

```bash
alembic upgrade head
```

6. **Запустите сервер разработки**

```bash
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

API будет доступен по адресу: http://localhost:8000

Swagger документация: http://localhost:8000/docs

## 🔐 Аутентификация

### Регистрация Yandex OAuth приложения

1. Перейдите на https://oauth.yandex.ru/
2. Создайте новое приложение
3. Укажите Redirect URI: `http://localhost:5173/auth/callback` (для разработки)
4. Скопируйте Client ID и Client Secret в `.env`

### Flow авторизации (Yandex ID Suggest)

**Yandex ID Suggest** - современная мгновенная авторизация:

1. **Фронтенд** подключает Yandex ID Suggest SDK и отображает виджет/кнопку
2. Если пользователь авторизован в Яндексе - видит свое имя и аватар
3. **Пользователь** кликает на виджет/кнопку (1 клик!)
4. **Yandex** мгновенно возвращает access token через iframe
5. **Фронтенд** отправляет токен на `POST /auth/yandex`
6. **Backend** валидирует токен, получает данные пользователя
7. **Backend** создает/находит пользователя в БД
8. **Backend** генерирует JWT токены и возвращает их
9. **Access token** отправляется в ответе, **refresh token** - в HTTP-only cookie

**Преимущества:**
- ⚡ Мгновенный вход (< 1 секунды)
- 👤 Персонализированный UI (показывает имя и аватар ДО клика)  
- 🎯 Один клик вместо нескольких
- 🚫 Без редиректов
- ✅ Рекомендовано Яндексом

### API эндпоинты авторизации

#### POST `/auth/yandex`
Авторизация через Yandex ID Suggest

**Request:**
```json
{
  "token": "access_token_from_yandex_suggest"
}
```

**Response:**
```json
{
  "user": {
    "id": "uuid",
    "display_name": "User Name",
    "avatar_url": "https://...",
    "created_at": "2026-01-09T15:00:00Z"
  },
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```


#### POST `/auth/refresh`
Обновление access токена

**Headers:**
- Cookie: `refresh_token=...`

**Response:**
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

#### POST `/auth/logout`
Выход из системы (удаляет refresh token cookie)

**Response:**
```json
{
  "message": "Successfully logged out"
}
```

#### GET `/auth/me`
Получить информацию о текущем пользователе

**Headers:**
- Authorization: `Bearer <access_token>`

**Response:**
```json
{
  "id": "uuid",
  "display_name": "User Name",
  "avatar_url": "https://...",
  "created_at": "2026-01-09T15:00:00Z"
}
```

## 🏗️ Архитектура

Проект следует принципам **Clean Architecture**:

```
app/
├── api/                    # Presentation layer
│   ├── dependencies.py     # FastAPI dependencies
│   ├── shemas/            # API request/response models
│   └── v1/routers/        # API endpoints
├── application/           # Business logic layer
│   └── auth/
│       ├── auth_service.py    # Auth business logic
│       └── auth_dto.py        # Internal DTOs
├── infrastructure/        # Infrastructure layer
│   ├── database/         # Database models & config
│   ├── repo/             # Repository implementations
│   └── auth/             # OAuth providers
├── core/                 # Core utilities
│   ├── config.py        # Configuration
│   └── secure.py        # Security utilities
├── di.py                # Dependency injection
└── main.py              # Application entry point
```

## 🗄️ Модель данных

### User
Пользователь системы

### AuthAccount
OAuth аккаунты пользователя (Yandex, Telegram)

### Project
Проект для организации сниппетов

### Folder
Папки внутри проекта (опционально)

### Snippet
Сниппет кода с тегами и full-text поиском

### Tag
Теги для категоризации сниппетов

## 📝 TODO

- [ ] Добавить Alembic миграции
- [ ] Реализовать CRUD для проектов
- [ ] Реализовать CRUD для сниппетов
- [ ] Реализовать систему тегов
- [ ] Реализовать полнотекстовый поиск
- [ ] Добавить rate limiting
- [ ] Добавить логирование запросов
- [ ] Добавить unit тесты
- [ ] Добавить integration тесты
- [ ] Добавить Dockerfile
- [ ] Настроить CI/CD

## 📄 Лицензия

MIT
