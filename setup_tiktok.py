#!/usr/bin/env python3
"""
TikTok Account Setup Scripts
Различные варианты авторизации TikTok
"""

import json
from pathlib import Path

CONFIG_DIR = Path('/home/emilAzure/.openclaw/workspace/projects/tiktok-publisher/config')
COOKIES_FILE = CONFIG_DIR / 'cookies.json'
CREDS_FILE = CONFIG_DIR / 'credentials.json'

print("🎵 TikTok Account Authorization Options")
print("=" * 70)
print()

# Check current auth status
if COOKIES_FILE.exists():
    with open(COOKIES_FILE, 'r') as f:
        cookies = json.load(f)
    print(f"✅ Cookies file exists: {len(cookies)} cookies found")
    print(f"📂 Location: {COOKIES_FILE}")
else:
    print(f"❌ Cookies file not found at: {COOKIES_FILE}")

print()
print("=" * 70)
print("🔐 AUTHORIZATION OPTIONS:")
print("=" * 70)
print()

print("""
Вариант 1: Вручную получить cookies (рекомендуется для headless systems)
────────────────────────────────────────────────────────────────────────
Этот метод требует доступа к браузеру (Chrome/Edge/Firefox) на компьютере:
   1. Откройте TikTok в браузере (www.tiktok.com)
   2. Войди в свой аккаунт вручную
   3. Открой DevTools (F12) → Application → Cookies → www.tiktok.com
   4. Скопируй все cookies в JSON формате
   5. Сохрани в файл cookies.json

Python script для импорта:
   python3 src/import_cookies.py
""")

print("""
Вариант 2: TikTok API Credentials (официальный способ)
────────────────────────────────────────────────────────────────────────
Для коммерческого использования:
   1. Перейди: https://developers.tiktok.com
   2. Создай приложение → Получи Client ID и Client Secret
   3. Получи access token через OAuth flow
   4. Сохрани в credentials.json

File format:
   {
     "client_id": "your_client_id",
     "client_secret": "your_client_secret",
     "access_token": "your_access_token"
   }
""")

print("""
Вариант 3: Local Browser Authorization (требует GUI)
────────────────────────────────────────────────────────────────────────
Если у тебя есть доступ к графическому интерфейсу:
   • Запусти authorize_tiktok.py
   • Откроется браузер для авторизации
   • Cookies сохранятся автоматически

Запуск:
   python3 authorize_tiktok.py
""")

print()
print("=" * 70)
print("⚙️  CURRENT STATUS:")
print("=" * 70)

if COOKIES_FILE.exists():
    print("✅ Method 1: Cookies - READY")
else:
    print("❌ Method 1: Cookies - NOT CONFIGURED")

print()

if CREDS_FILE.exists():
    print("✅ Method 2: API - READY")
else:
    print("❌ Method 2: API - NOT CONFIGURED")

print()

print("ℹ️  Method 3: Local GUI - Requires graphical interface (not available)")
print()

print("=" * 70)
print("📋 RECOMMENDED ACTION:")
print("=" * 70)
print()
print("Для настройки авторизированной TikTok публикации:")
print()
print("1. Войди в TikTok в своём браузере")
print("2. Открой DevTools (F12) → Application → Cookies → tiktok.com")
print("3. Скопируй все cookies и сохрани как JSON")
print("4. Я помогу импортировать cookies в систему")
print()
print("💡 Если хочешь начать сейчас, просто скажи:")
print("   '🍪 Вот cookies: {}' и я настрим авторизацию!")
print("=" * 70)
print()

# Create empty config file if not exists
if not CREDS_FILE.exists():
    CREDS_FILE.parent.mkdir(exist_ok=True)
    with open(CREDS_FILE, 'w') as f:
        json.dump({
            "mode": "playwright",
            "username": "",
            "status": "not_configured"
        }, f, indent=2)
    print(f"✓ Created empty credentials template: {CREDS_FILE}")

print()
print("✅ Setup complete! Ready for TikTok upload configuration.")
print()
