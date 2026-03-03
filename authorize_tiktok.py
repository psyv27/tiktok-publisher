#!/usr/bin/env python3
"""
TikTok Account Authorization Script
Открывает браузер для ручной авторизации в TikTok и сохраняет cookies
"""

import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

COOKIES_FILE = Path('/home/emilAzure/.openclaw/workspace/projects/tiktok-publisher/config/cookies.json')
COOKIES_FILE.parent.mkdir(exist_ok=True)

def authorize_account():
    """Открывает TikTok в headed mode для ручной авторизации"""

    print("🎵 TikTok Account Authorization")
    print("=" * 60)
    print()

    with sync_playwright() as p:
        print("🌐 Launching chromium browser...")

        browser = p.chromium.launch(
            headless=False,  # Визуальный режим для ручной авторизации
            slow_mo=1000      # Медленное действие для наглядности
        )

        # Create context with realistic user agent
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080},
            locale='en-US',
            timezone_id='America/New_York'
        )

        print("📱 Opening TikTok...")

        page = context.new_page()

        # Go to TikTok
        page.goto('https://www.tiktok.com/', wait_until='networkidle')

        print()
        print("=" * 60)
        print("🔐 MANUAL AUTHORIZATION REQUIRED")
        print("=" * 60)
        print()
        print("✅ Browser launched successfully!")
        print("📱 TikTok website is open")
        print()
        print("⚠️  STEPS TO COMPLETE:")
        print("   1. Click 'Log in' button on TikTok")
        print("   2. Login with your TikTok account")
        print("   3. Verify your email/phone if required")
        print("   4. Make sure you see the TikTok feed")
        print()
        print("⏳ I will wait for you to complete login...")
        print("   🔹 Type 'done' here and press Enter when you're finished")
        print("=" * 60)
        print()
        print("💡 TIPS:")
        print("   • Use email/phone login (easier than OAuth)")
        print("   • Keep the browser window open")
        print("   • Wait for homepage to fully load")
        print("=" * 60)
        print()

        # Wait for user to complete login
        input("   👉 Press Enter when login is done... ")

        print()
        print("🍪 Saving cookies...")

        # Save authenticated cookies
        cookies = context.cookies()
        with open(COOKIES_FILE, 'w') as f:
            json.dump(cookies, f, indent=2)

        print("✅ Cookies saved successfully!")
        print(f"📂 Location: {COOKIES_FILE}")
        print()

        # Verify login
        try:
            # Try to access TikTok homepage again with cookies
            page.goto('https://www.tiktok.com/', wait_until='networkidle')

            # Check if we're logged in (look for user profile or logout)
            logged_in = bool(page.locator('[data-e2e="top-nav-item-profile"]').count() > 0)

            if logged_in:
                print("✅ LOGIN VERIFIED! Account is successfully authenticated!")

                # Get username
                try:
                    profile_btn = page.locator('[data-e2e="top-nav-item-profile"]')
                    username = profile_btn.inner_text() if profile_btn.count() > 0 else "Unknown"
                    print(f"👤 Account: {username}")
                except:
                    pass
            else:
                print("⚠️  Could not verify login. Please check if you're actually logged in.")

        except Exception as e:
            print(f"⚠️  Verification failed: {e}")

        print()
        print("=" * 60)
        print("✅ AUTHORIZATION COMPLETE")
        print("=" * 60)
        print()
        print("📋 What's next:")
        print("   1. Cookies are saved and can be used for uploads")
        print("   2. Run TikTok uploader script (headless mode)")
        print("   3. Videos will be uploaded to your account")
        print()
        print("💡 To upload videos later, use:")
        print("   python3 src/tiktok_bot.py <video_path> [caption] [hashtags]")
        print("=" * 60)

        # Keep browser open temporarily for user to verify
        print()
        print("⏳ Keeping browser open for 10 seconds for verification...")
        time.sleep(10)

        browser.close()

        return True

if __name__ == '__main__':
    try:
        authorize_account()
        print()
        print("✨ Authorization process completed successfully!")
    except KeyboardInterrupt:
        print("\n⚠️  Authorization interrupted by user")
    except Exception as e:
        print(f"❌ Authorization failed: {e}")
        import traceback
        traceback.print_exc()
