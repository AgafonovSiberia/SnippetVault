# Быстрый старт - SnippetVault Frontend

## Краткое описание

Вы находитесь в папке `web/` - это Frontend часть приложения SnippetVault, построенная на **React + TypeScript + Material UI**.

## 🚀 Запуск за 3 шага

### 1. Установите зависимости

```bash
npm install
```

### 2. Настройте Yandex ID

Скопируйте `.env.example` в `.env`:
```bash
cp .env.example .env
```

Получите Client ID на [Yandex OAuth](https://oauth.yandex.ru/) и укажите его в `.env`:
```env
VITE_YANDEX_CLIENT_ID=ваш_yandex_client_id
```

### 3. Запустите dev-сервер

```bash
npm run dev
```

Откройте http://localhost:5173

## 📂 Что внутри?

```
web/
├── src/
│   ├── components/       # React компоненты
│   │   ├── auth/        # YandexIDButton
│   │   └── common/      # Loading и др.
│   ├── pages/           # Страницы
│   │   ├── Auth/        # LoginPage
│   │   └── Dashboard/   # DashboardPage
│   ├── services/        # API клиенты
│   ├── hooks/           # useAuth и др.
│   ├── types/           # TypeScript типы
│   ├── utils/           # Yandex ID SDK
│   └── theme/           # Material UI тема
├── docs/                # Документация
└── .env                 # Переменные окружения
```

## 🔑 Основные файлы

| Файл | Описание |
|------|----------|
| `src/App.tsx` | Главный компонент + роутинг |
| `src/pages/Auth/LoginPage.tsx` | Страница авторизации |
| `src/components/auth/YandexIDButton.tsx` | Виджет Yandex ID |
| `src/services/auth.service.ts` | API авторизации |
| `src/hooks/useAuth.ts` | Хук управления авторизацией |

## 🎨 Технологии

- ⚛️ React 19
- 🔷 TypeScript
- 🎨 Material UI (темная тема)
- 🚀 Vite
- 🔐 Yandex ID OAuth

## 📚 Дополнительная документация

- [README.md](./README.md) - Полная документация
- [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md) - Архитектура
- [docs/YANDEX_ID_INTEGRATION.md](./docs/YANDEX_ID_INTEGRATION.md) - Интеграция с Yandex ID

## ❓ Частые вопросы

### Как получить Yandex Client ID?

1. Перейдите на https://oauth.yandex.ru/
2. Создайте новое приложение
3. Укажите Redirect URI: `http://localhost:5173/`
4. Скопируйте Client ID в `.env`

### Backend не отвечает?

Убедитесь, что backend запущен на `http://localhost:8000`:
```bash
cd ../
docker compose up backend
```

### Как собрать production версию?

```bash
npm run build
```

Файлы будут в папке `dist/`

## 🐛 Отладка

### Открыть DevTools

В браузере: `F12` или `Ctrl+Shift+I`

### Проверить API запросы

В DevTools → Network → проверьте запросы к `/api/v1/auth/*`

### Проверить токены

В DevTools → Application → Local Storage → проверьте `access_token`

## 🎯 Следующие шаги

1. ✅ Запустили приложение
2. ✅ Настроили Yandex ID
3. 🔲 Протестировали авторизацию
4. 🔲 Изучили архитектуру
5. 🔲 Начали разработку новых фич

## 💬 Нужна помощь?

Изучите документацию в папке `docs/` или посмотрите код - он хорошо задокументирован!

---

**Удачной разработки! 🚀**
