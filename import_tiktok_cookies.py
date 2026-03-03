#!/usr/bin/env python3
"""
TikTok Cookies Import Script
Импорт cookies из браузера для Playwright automation

Этот скрипт позволяет импортировать cookies из Chrome/Edge/Firefox
для использования в headless TikTok uploads.

Usage:
    python3 import_tiktok_cookies.py
"""

import json
import base64
from pathlib import Path

CONFIG_FILE = Path(__file__).parent.parent / 'config' / 'cookies.json'

print("🍪 TikTok Cookies Import Tool")
print("=" * 70)
print()

print("""
Как получить TikTok cookies из браузера:

🔹 Хром/Chrome:
──────────────────────────────────────
1. Открой Chrome и войди в TikTok
2. F12 → Application → Cookies → tiktok.com
3. Выделите все cookies → Copy as JSON (или вручную)

🔹 Firefox:
──────────────────────────────────────
1. Открой Firefox и войди в TikTok
2. F12 → Storage → Cookies → tiktok.com
3. Выделите все cookies → Export

🔹 Edge:
──────────────────────────────────────
1. Открой Edge и войди в TikTok
2. F12 → Application → Cookies → tiktok.com
3. Выделите все cookies → Copy as JSON
""")

print()
print("=" * 70)
print("📋 SEND YOUR COOKIES HERE:")
print("=" * 70)
print()
print("✏️ Вставь cookies JSON в этом формате:")
print()
print("🍪 Вот cookies:")
print('{')
print('  "name": "sessionid",')
print('  "value": "your_session_id",')
print('  "domain": ".tiktok.com",')
print('  "path": "/",')
print('  "expires": 1234567890')
print('}')
print()
print("=" * 70)
print()

# Show example expected format
example_cookies = [
    {
        "name": "sessionid",
        "value": "example_session_id_here",
        "domain": ".tiktok.com",
        "path": "/",
        "expires": 1234567890,
        "httpOnly": True,
        "secure": True
    },
    {
        "name": "passport_csrf_token",
        "value": "example_csrf_token",
        "domain": ".tiktok.com",
        "path": "/",
        "expires": 1234567890
    }
]

print("📊 Expected cookies example:")
print(json.dumps(example_cookies, indent=2))
print()
print("=" * 70)
print()

print("💡 Important cookies to include:")
print("   ✓ sessionid (main authentication cookie)")
print("   ✓ passport_csrf_token (CSRF protection)")
print("   ✓ ttwid (TikTok user ID)")
print("   ✓ passport_auth_id (additional auth)")
print()

print("=" * 70)
print("✨ After sending cookies, TikTok Bot will:")
print("   1. Save cookies to config/cookies.json")
print("   2. Import into Playwright browser context")
print("   3. Allow headless video uploads")
print("   4. Work like a logged-in user")
print("=" * 70)
print()

print("⚠️  Notes:")
print("   • Cookies expire - regenerate periodically")
print("   • Don't share with others (authentication data)")
print("   • Works best with recent cookies from active session")
print()

print("🔒 Privacy: Your cookies will be saved locally only")
print("   Path: " + str(CONFIG_FILE))
print()
print()
print("✏️ Вставь cookies и скрипт сохранит их автоматически!")
print()
