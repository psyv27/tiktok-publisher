# 🍪 TIKTOK COOKIES IMPORT GUIDE

🎵 Получение и импорт TikTok cookies для Playwright automation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 ПОШАГОВАЯ ИНСТРУКЦИЯ

🔹 STEP 1: Вход в TikTok
────────────────────────────────────────────────
1. Открой TikTok в браузере (Chrome, Firefox, или Edge)
   → https://www.tiktok.com

2. Войди в свой аккаунт
   → Email/phone или TikTok аккаунт

3. Убедись что ты на главной странице TikTok
   → Должно быть видно видео и ленту

🔹 STEP 2: Извлечение Cookies
────────────────────────────────────────────────
Для Chrome:
1. Нажми F12 → откроется DevTools
2. Нажми "Application" tab (или "Приложения" в русской версии)
3. Разверни "Cookies" → выбери "https://www.tiktok.com"
4. Выдели все cookies → правая кнопка → "Copy as JSON"

Для Firefox:
1. Нажми F12 → Storage tab
2. Cookies → tiktok.com
3. Выдели все cookies → правая кнопка → "Export"

Для Edge:
1. F12 → Application tab
2. Cookies → tiktok.com
3. Copy as JSON

🔹 STEP 3: Отправка Cookies
────────────────────────────────────────────────
Отошли cookies в чат в формате JSON:

🍪 Вот cookies:
[
  {
    "name": "sessionid",
    "value": "your_session_id_here",
    "domain": ".tiktok.com",
    "path": "/",
    "expires": 1234567890
  },
  {
    "name": "passport_csrf_token",
    "value": "your_csrf_token_here",
    "domain": ".tiktok.com",
    "path": "/",
    "expires": 1234567890
  }
]

ИЛИ можно отправить напрямую:
🍪 Вот cookies: [{"name": "sessionid", "value": "...", ...}]

🔹 STEP 4: Автоматическое сохранение
────────────────────────────────────────────────
Клэв автоматически:
1. Сохранит cookies в config/cookies.json
2. Обновит конфигурацию TikTok бота
3. Подтвердит импорт

✨ После этого TikTok Bot готов к загрузке видео!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔍 ВАЖНЫЕ COOKIES

Обязательно включи следующие cookies:
✓ sessionid - основной authentication cookie
✓ passport_csrf_token - защита CSRF
✓ ttwid - TikTok user ID
✓ passport_auth_id - дополнительная аутентификация
✓ sid_tt - session identifier
✓ passport_fe_beating_key - heartbeat cookie

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 ТЕСТИРОВАНИЕ

После импорта cookies, проверь:
┌─────────────────────────────────────────────────────────────────┐
│ python3 src/tiktok_bot.py --test                               │
│ → Протестирует подключение к TikTok через cookies                │
└─────────────────────────────────────────────────────────────────┘

🚀 Загрузка видео:
┌─────────────────────────────────────────────────────────────────┐
│ python3 src/tiktok_bot.py video.mp4 "Caption!" #foryou #viral   │
│ → Загрузит видео на TikTok                                      │
└─────────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 СОВЕТЫ

✅ Получи cookies ПОСЛЕ входа в TikTok
✅ Cookies с свежей сессии работают лучше
✅ Экспортируй ВСЕ cookies для tiktok.com
✅ Не забудь про .tiktok.com (с точкой впереди)

⚠️ Cookies истекают - обновляй периодически
⚠️ Не отправляй cookies другим людям
⚠️ Клэв сохранит cookies локально только в config/

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❓ ВАРИАНТЫ

Если не можешь получить cookies:
🎯 Использовать TikTok Web Interface напрямую
   • Скрипт откроет браузер для ручной авторизации
   • После логина cookies сохраняются автоматически
   • Требуется графический интерфейс (не работает в headless)

🎯 Использовать OAuth API (в разработке)
   • Официальный TikTok API
   • Требует access token от OAuth Playground
   • Internal server error (текущая проблема)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✨ ГОТОВ К IMPORT!

Открой TikTok, войди, получи cookies и пришли сюда!

🍪 Жду cookies от тебя!
