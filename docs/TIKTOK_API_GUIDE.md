#!/bin/bash
# TikTok API Registration Guide
# Пошаговое руководство для получения TikTok API credentials

cat << 'EOF'
🎵 TIKTOK API REGISTRATION GUIDE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Шаги для получения TikTok API Credentials:

🔹 STEP 1: Регистрация TikTok Developer Account
─────────────────────────────────────────────
1. Перейди на: https://developers.tiktok.com

2. Нажми "Developer Portal" или "Log In"

3. Войди используя свой TikTok аккаунт
   • Можно использовать email/phone или TikTok аккаунт

4. Подтверди email если требуется


🔹 STEP 2: Создание приложения
─────────────────────────────────────
1. Нажми "Create app" или "Get Started"

2. Выбери тип приложения:
   • "Creator Tools" для блогеров
   или
   • "Business Suite" для бизнеса

3. Заполни форму:
   App Name: "Video Publisher Bot"
   Description: "Bot для публикации коротких видео с TikTok на YouTube"
   Industry: "Entertainment" или "Technology"

4. Выбри платформы:
   ✓ Website (Localhost:3000 для разработки)

5. Заполни необходимые данные и отправь на проверку


🔹 STEP 3: Разработка и Testing (Проверка)
─────────────────────────────────────────────
1. После создания приложение будет в "Testing" состоянии

2. Найди "Client ID" и "Client Secret":
   Настройки приложения → Keys and tokens

3. Copy следующие значения:
   • Client ID (обычно starts with "aw_")
   • Client Secret (длинная строка)

4. Настрой Redirect URI:
   • Добавь: http://localhost:3000/callback
   • Или если нет localhost: http://example.com/callback


🔹 STEP 4: Получение Access Token
─────────────────────────────────────
После создания app и получения Client ID:

Вариант A: Использовать TikTok's OAuth Playground
────────────────────────────────────────────────
1. Перейди: https://developers.tiktok.com/oauth/playground/

2. Введи Client ID
3. Выбери scopes:
   ✓ video.list
   ✓ video.create
   ✓ video.publish

4. Нажми "Get Access Token"
5. Скопируй полученный access token

Вариант B: Программная авторизация
────────────────────────────────────────────────
Используй OAuth flow с redirect_uri

3. Copy полученный access token


🔹 STEP 5: Конфигурация проекта
─────────────────────────────────────────────
Когда получены все credentials, запиши их:

File: config/api_credentials.json

{
  "mode": "api",
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET",
  "access_token": "YOUR_ACCESS_TOKEN",
  "redirect_uri": "http://localhost:3000/callback",
  "scopes": ["video.list", "video.create", "video.publish"],
  "status": "configured"
}


🔹 ВАЖНОЕ:
─────────────────────────────────────
⚠️  Client Secret должен быть секретным! Не отправляй его публично!
⚠️  Access Tokens обычно истекают (24 часа для testing токенов)
⚠️  For production: Implement refresh token flow
⚠️  API Limits: Testing mode имеет пределы запросов


✨ После получения credentials просто напиши мне:

🔑 Вот мои credentials:

{
  "client_id": "aw_XXXXXX",
  "client_secret": "XXXXXXXX",
  "access_token": "XXXXXXXX"
}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 Дополнительные ресурсы:
• API Documentation: https://developers.tiktok.com/doc/video-upload
• OAuth Guide: https://developers.tiktok.com/doc/getting-started-with-oauth-2
• Video Upload API: https://developers.tiktok.com/doc/video-upload-api/

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Когда будешь готов, отправь мне credentials и я настрою TikTok Publisher!

---

💡 Для начала можно использовать токен в Testing Stage
   (ограничения apply, но достаточно для тестирования)

EOF
