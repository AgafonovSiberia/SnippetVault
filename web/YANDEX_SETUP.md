# 🔧 Инструкция по настройке Yandex ID

## ⚠️ ВАЖНО: Требуется HTTPS!

Yandex ID SDK **требует HTTPS** для корректной работы виджетов авторизации. Современные браузеры блокируют сторонние cookies (third-party cookies) для HTTP соединений, что приводит к ошибке `not_available` даже если вы авторизованы в Яндексе.

**📖 Полная инструкция по настройке HTTPS:** См. файл [`YANDEX_HTTPS_SETUP.md`](./YANDEX_HTTPS_SETUP.md)

---

## Проблема
Виджет Yandex ID не отображается (показывается fallback кнопка) из-за блокировки сторонних cookies в HTTP режиме.

## ✅ Решение

### Шаг 1: Обновите файл `web/.env`

Убедитесь, что файл `web/.env` содержит **HTTPS** URL:

```env
# API Configuration
VITE_API_URL=/api

# Yandex ID Configuration
VITE_YANDEX_CLIENT_ID=44d799edfaaa407eb79fb0eafed36a44
VITE_YANDEX_REDIRECT_URI=https://localhost:5173/
```

**ВАЖНО:** 
- Используйте **`https://localhost:5173/`**, а НЕ `http://`!
- `VITE_YANDEX_REDIRECT_URI` должен совпадать с тем, что указано в консоли Yandex OAuth
- Обратите внимание на завершающий слеш `/`

### Шаг 2: Настройте приложение в Yandex OAuth

1. Откройте https://oauth.yandex.ru/
2. Выберите ваше приложение (Client ID: `44d799edfaaa407eb79fb0eafed36a44`)
3. Перейдите в раздел **"Платформы"** → **"Веб-сервисы"**
4. В поле **"Callback URI"** добавьте:
   ```
   https://localhost:5173/
   ```
5. Сохраните изменения

### Шаг 3: Проверьте разрешения

В разделе **"Доступ к данным"** должны быть отмечены:
- ✅ Аватар пользователя
- ✅ Имя и фамилия  
- ✅ Логин

### Шаг 4: Перезапустите dev-сервер

```bash
# Остановите текущий сервер (Ctrl+C)
# Затем запустите снова:
npm run dev
```

**ВАЖНО:** После изменения `.env` файла Vite автоматически перезапускается, но лучше полностью остановить и запустить заново.

### Шаг 5: Очистите кэш браузера

1. Откройте DevTools (F12)
2. Правой кнопкой по кнопке обновления
3. Выберите **"Очистить кэш и выполнить жесткую перезагрузку"**

## 🔍 Диагностика

### Проверьте, что Client ID загружен правильно:

Откройте консоль браузера (F12) и выполните:

```javascript
// Найти iframe Яндекса
const iframe = document.querySelector('iframe[src*="yandex.ru"]');
console.log('Iframe src:', iframe?.src);

// Извлечь параметры
if (iframe) {
  const url = new URL(iframe.src);
  console.log('Client ID:', url.searchParams.get('client_id'));
  console.log('Redirect URI:', url.searchParams.get('redirect_uri'));
}
```

**Ожидаемый результат:**
```
Client ID: 44d799edfaaa407eb79fb0eafed36a44
Redirect URI: https://localhost:5173/
```

### Проверьте ошибки в консоли:

Если видите ошибку `Refused to display ... in a frame` - это значит, что:
1. Redirect URI не совпадает с тем, что указан в Yandex OAuth
2. Или Client ID недействителен
3. Или приложение заблокировано в консоли Яндекса

## 📋 Checklist

- [ ] В `web/.env` указан правильный `VITE_YANDEX_CLIENT_ID`
- [ ] В `web/.env` указан `VITE_YANDEX_REDIRECT_URI=https://localhost:5173/`
- [ ] В консоли Yandex OAuth добавлен Callback URI: `https://localhost:5173/`
- [ ] Dev-сервер перезапущен
- [ ] Кэш браузера очищен
- [ ] В консоли браузера нет ошибки "Refused to display in a frame"

## 🎯 Результат

После выполнения всех шагов:
- ✅ Если вы **залогинены в Яндексе** → отображается **Suggest Widget** с вашим аватаром
- ✅ Если вы **НЕ залогинены** → отображается **Button Widget** или fallback кнопка

---

**Если проблема сохраняется:**
1. Проверьте, что приложение в статусе "В разработке" или "Опубликовано" в консоли Яндекса
2. Убедитесь, что используете тот же Client ID, что и в консоли
3. Проверьте, что redirect_uri точно совпадает (включая протокол, порт и слеш)
