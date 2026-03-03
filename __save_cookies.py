#!/usr/bin/env python3
"""
TikTok Cookies Parser and Saver
Принимает cookies JSON от пользователя, сохраняет в config
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

COOKIES_FILE = Path(__file__).parent.parent / 'config' / 'cookies.json'
CONFIG_FILE = Path(__file__).parent.parent / 'config' / 'config.json'

def parse_cookies_input(text):
    """Parse cookies from user text input"""

    # Remove common wrappers
    text = text.strip()
    if text.startswith('🍪 Вот cookies:'):
        text = text[15:].strip()

    try:
        # Try to parse as JSON
        cookies = json.loads(text)

        # If it's a single cookie (dict), wrap in array
        if isinstance(cookies, dict):
            cookies = [cookies]

        return cookies
    except json.JSONDecodeError:
        print("❌ Invalid JSON format. Please send cookies in JSON format.")
        return None

def save_cookies(cookies):
    """Save cookies to config file"""

    # Ensure required fields
    for cookie in cookies:
        if 'domain' not in cookie:
            cookie['domain'] = '.tiktok.com'
        if 'path' not in cookie:
            cookie['path'] = '/'
        if 'expires' not in cookie:
            # Set default expiry (30 days)
            cookie['expires'] = int((datetime.now() + timedelta(days=30)).timestamp())

    # Save cookies
    COOKIES_FILE.parent.mkdir(exist_ok=True)

    with open(COOKIES_FILE, 'w') as f:
        json.dump(cookies, f, indent=2)

    return True

def update_config_cookies_path():
    """Update config.json with cookies path"""

    CONFIG_FILE.parent.mkdir(exist_ok=True)

    config = {}
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)

    config['cookies_path'] = str(COOKIES_FILE)
    config['last_cookies_update'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

    return True

def display_cookies_status(cookies):
    """Display cookies info"""

    print()
    print("=" * 70)
    print("✅ TIKTOK COOKIES SAVED!")
    print("=" * 70)
    print()
    print(f"📂 File: {COOKIES_FILE}")
    print(f"🔢 Total cookies: {len(cookies)}")
    print()
    print("🍪 Cookies list:")
    for i, cookie in enumerate(cookies, 1):
        name = cookie.get('name', 'unknown')
        domain = cookie.get('domain', '.tiktok.com')
        value_len = len(cookie.get('value', ''))
        print(f"   {i}. {name} (@{domain}) - {value_len} chars")
    print()
    print("=" * 70)
    print("🚀 TIKTOK BOT READY!")
    print("=" * 70)
    print()
    print("✨ Now you can upload videos:")
    print()
    print("   python3 src/tiktok_bot.py video.mp4 \"Caption!\" #foryou #viral")
    print()
    print("💡 Cookies expire periodically. Replace when needed:")
    print("   1. Open TikTok in browser")
    print("   2. Get new cookies")
    print("   3. Re-import using same method")
    print("=" * 70)
    print()

def main():
    """Main function"""

    print("🍪 TikTok Cookies Import Tool")
    print("=" * 70)
    print()

    # If argument provided, use it directly
    if len(sys.argv) > 1:
        cookies_text = ' '.join(sys.argv[1:])
    else:
        print("⏳ Waiting for cookies input...")
        print("   (Paste JSON cookies and press Enter)")
        print()
        cookies_text = input("🍪 Cookies: ").strip()

    if not cookies_text:
        print("❌ No cookies provided!")
        return False

    # Parse cookies
    cookies = parse_cookies_input(cookies_text)
    if not cookies:
        return False

    # Save cookies
    if not save_cookies(cookies):
        return False

    # Update config
    if not update_config_cookies_path():
        return False

    # Display status
    display_cookies_status(cookies)

    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
