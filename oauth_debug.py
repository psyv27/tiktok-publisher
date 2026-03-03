#!/usr/bin/env python3
"""
TikTok OAuth Debug Script
Проверка credentials и OAuth flow
"""

import json
import requests
from pathlib import Path

# Load credentials
config_path = Path(__file__).parent / 'config' / 'api_credentials.json'
with open(config_path, 'r') as f:
    config = json.load(f)

print("🔍 TikTok OAuth Debug")
print("=" * 70)
print()

client_id = config.get('client_id')
client_secret = config.get('client_secret')
redirect_uri = config.get('redirect_uri')

print("📋 Current Configuration:")
print(f"Client ID: {client_id}")
print(f"Client Secret: {client_secret[:10]}...{client_secret[-10:]}")
print(f"Redirect URI: {redirect_uri}")
print()

# Try different redirect URI options
redirect_options = [
    "https://oauth.pstmn.io/v1/callback",
    "https://oauth2.code-artifacts.com/callback",
    "https://example.com/callback",
    "https://developers.tiktok.com/oauth/callback"
]

print("🔄 Alternative Redirect URIs to try:")
print("=" * 70)
for i, uri in enumerate(redirect_options, 1):
    print(f"{i}. {uri}")
print()

print("📌 The 'internal server error' might be due to:")
print("  ❌ Incorrect redirect URI format")
print("  ❌ TikTok API Playground temporarily down")
print("  ❌ App permissions not granted")
print("  ❌ Client ID/Secret mismatch")
print()

print("=" * 70)
print("💡 Alternative Solutions:")
print("=" * 70)
print()

print("""
🎯 OPTION 1: Use TikTok Web-based Auth (Manual)
─────────────────────────────────────────────────
Instead of OAuth Playground, try browser-based flow:

1. Go to: https://developers.tiktok.com/app/
   → Find your app "Video Publisher Bot"

2. Click "Manage" on your app

3. Go to "API Keys" or "Manage Keys"

4. Try to generate access token directly there

5. Some apps allow token generation without OAuth flow

─────────────────────────────────────────────────

🎯 OPTION 2: Use TikTok Business Suite
─────────────────────────────────────────────────
1. Business Suite App: https://business.tiktok.com/
2. Manage Integrations → Create Integration
3. Get access token from dashboard

─────────────────────────────────────────────────

🎯 OPTION 3: Use Automated OAuth Flow with Real Redirect
─────────────────────────────────────────────────
If you have a domain/VPS, we can set up real callback:

1. Create simple callback page (HTML/JS)
2. Host on your domain
3. Configure in TikTok app
4. Run auto OAuth flow

─────────────────────────────────────────────────

🎯 OPTION 4: Create New App (Quick Fix)
─────────────────────────────────────────────────
Sometimes apps get stuck in testing mode:
1. Delete current "Video Publisher Bot" app
2. Create brand new app on TikTok Developers
3. Use different App Name (e.g., "TikTok Publisher v2")
4. Get new Client ID and Secret
5. Try OAuth Playground again

─────────────────────────────────────────────────

""")

print("=" * 70)
print("✅ Temporary Workaround:")
print("=" * 70)
print()
print("If you're just TESTING (not production), we could:")
print()
print("🎵 Use TikTok Browser Automation (Playwright)")
print("   • Login directly to browser")
print("   • Upload videos like a human would")
print("   • More complex but doesn't need API tokens")
print()
print("🔧 Switch to Browser Mode:")
print("   python3 src/tiktok_bot.py video.mp4 --caption \"text\"")
print()
print("=" * 70)
