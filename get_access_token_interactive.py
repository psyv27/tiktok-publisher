#!/usr/bin/env python3
"""
TikTok OAuth Access Token - Auto Fetch Script

Этот скрипт упрощает получение TikTok Access Token через браузер.

Требования:
- X Server или X11 forwarding (ssh -X)
- Или Headless mode с взаимодействием

Использование:
1. Запустить скрипт: python3 get_access_token_interactive.py
2. Браузер откроется с TikTok OAuth Playground
3. Авторизуйся в TikTok аккаунт
4. Разреши доступ
5. Токен будет сохранен и выведен
"""

import asyncio
import re
from pathlib import Path
from playwright.async_api import async_playwright

# TikTok OAuth Settings
CLIENT_ID = "sbaws49sqt018swoyo"
CLIENT_SECRET = "4M6pKGeOUnJa6CtZ4GEaIBQvr4NZfqeu"
OAUTH_URL = "https://developers.tiktok.com/oauth/playground/"
REDIRECT_URI = "https://oauth.pstmn.io/v1/callback"  # Postman callback
SCOPES = "video.publish,video.create,video.list"

# Output paths
WORKSPACE = Path("/home/emilAzure/.openclaw/workspace")
CREDENTIALS_FILE = WORKSPACE / "projects/tiktok-publisher/config/api_credentials.json"
TOKEN_FILE = WORKSPACE / "projects/tiktok-publisher/config/access_token.txt"


async def get_token_playwright():
    """Получить access token через Playwright"""

    print("=" * 70)
    print("🎵 TIKTOK OAUTH - ACCESS TOKEN FETCHER")
    print("=" * 70)
    print()
    print(f"📌 Client ID:     {CLIENT_ID}")
    print(f"📌 Redirect URI:  {REDIRECT_URI}")
    print(f"📌 Scopes:        {SCOPES}")
    print()
    print("=" * 70)
    print("🚀 Запускаю браузер для авторизации...")
    print()
    print("⚠️  ОЖИДАНИЕ:")
    print("   1. Откроется TikTok OAuth Playground")
    print("   2. Введи Client ID (если нужно)")
    print("   3. Авторизуйся в TikTok")
    print("   4. Разреши доступ")
    print("   5. Скрипт получит токен автоматически")
    print()
    print("=" * 70)
    input("\n🔑 Нажми Enter когда готов...")

    async with async_playwright() as p:
        # Запускаем браузер (headless=False нужно чтобы видеть сайт)
        browser = await p.chromium.launch(
            headless=False,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )

        # Если XServer недоступен - показать headless режим warning
        try:
            context = await browser.new_context()
            page = await context.new_page()
        except Exception as e:
            print(f"❌ Ошибка браузера: {e}")
            print()
            print("💡 РЕШЕНИЕ:")
            print("   1. Подключись через SSH с X11 forwarding:")
            print("      ssh -X user@server")
            print()
            print("   2. Или используй headless mode:")
            print("      python3 get_access_token_headless.py")
            print()
            await browser.close()
            return None

        # Navigate к TikTok OAuth Playground
        print()
        print("🌐 Открываю TikTok OAuth Playground...")
        print()

        try:
            await page.goto(OAUTH_URL, wait_until="networkidle", timeout=30000)
            print("✅ Страница загружена!")

            # Ждем авторизацию
            print()
            print("⏳ Жду авторизацию...")
            print("   Авторизуйся в TikTok и разреши доступ")
            print()
            print("   Токен появится на странице автоматически")
            print("   Скрипт перехватит его")

            # Подождим и ищем токен на странице
            await asyncio.sleep(5)

            # Перехватываем URL или ищем токен на странице
            # OAuth redirect обычно содержит access_token в URL
            max_wait = 300  # 5 минут на авторизацию
            waited = 0

            while waited < max_wait:
                # Проверяем URL
                url = page.url
                if "access_token" in url:
                    print()
                    print("✅ Токен найден в URL!")
                    access_token = re.search(r'access_token=([a-zA-Z0-9_-]+)', url)
                    if access_token:
                        token = access_token.group(1)
                        await save_token(token)
                        print()
                        print(f"🎉 ACCESS TOKEN: {token[:50]}...")
                        print()
                        print(f"💾 Сохранен в: {TOKEN_FILE}")
                        await browser.close()
                        return token

                # Проверяем content страницы
                content = await page.content()
                if "access_token" in content:
                    print()
                    print("✅ Токен найден на странице!")
                    match = re.search(r'"access_token":\s*"([a-zA-Z0-9_-]+)"', content)
                    if match:
                        token = match.group(1)
                        await save_token(token)
                        print()
                        print(f"🎉 ACCESS TOKEN: {token[:50]}...")
                        print()
                        print(f"💾 Сохранен в: {TOKEN_FILE}")
                        await browser.close()
                        return token

                await asyncio.sleep(2)
                waited += 2

            print()
            print("❌ Токен не найден в течение 5 минут")
            print()
            print("💡 Попробуй найти токен вручную на странице")
            print()

        except Exception as e:
            print(f"❌ Ошибка: {e}")
            import traceback
            traceback.print_exc()

        # Закрыть браузер через 2 секунды
        await asyncio.sleep(2)
        await browser.close()

    return None


async def save_token(token):
    """Сохранить токен в файл"""

    # Сохранить токен
    TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    TOKEN_FILE.write_text(token.strip())
    print(f"💾 Токен сохранен: {TOKEN_FILE}")

    # Обновить credentials файл
    if CREDENTIALS_FILE.exists():
        import json
        creds = json.loads(CREDENTIALS_FILE.read_text())
        creds["tiktok"]["access_token"] = token
        creds["tiktok"]["token_status"] = "connected"
        CREDENTIALS_FILE.write_text(json.dumps(creds, indent=2))
        print(f"💾 Credentials обновлен: {CREDENTIALS_FILE}")


def main():
    """Запуск"""

    print("=" * 70)
    print("🎵 TIKTOK ACCESS TOKEN - INTERACTIVE FETCH")
    print("=" * 70)
    print()
    print("📋 Этот скрипт поможет тебе получить Access Token для TikTok API")
    print()
    print("🚀 Требуется:")
    print("   • SSH соединение с X11 forwarding (ssh -X)")
    print("   • Или X Server на сервере")
    print()

    try:
        token = asyncio.run(get_token_playwright())

        if token:
            print()
            print("=" * 70)
            print("✅ Успешно!")
            print("=" * 70)
            print()
            print(f"🎵 ACCESS TOKEN: {token}")
            print()
            print("Теперь TikTok Publisher готов к работе! 🚀")
        else:
            print()
            print("=" * 70)
            print("❌ Не удалось получить токен")
            print("=" * 70)
            print()
            print("💡 Попробуй получить токен вручную:")
            print("   1. https://developers.tiktok.com/oauth/playground/")
            print("   2. Вставь Client ID: sbaws49sqt018swoyo")
            print("   3. Авторизуйся и получи токен")
            print("   4. Используй set_access_token.py для установки")
            print()

    except KeyboardInterrupt:
        print()
        print()
        print("❌ Прервано пользователем")
        print()
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
