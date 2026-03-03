#!/usr/bin/env python3
"""
Exchange authorization code for access token (for video.upload - drafts)
"""
import requests
import json

# TikTok OAuth credentials
CLIENT_ID = "sbaws49sqt018swoyo"
CLIENT_SECRET = "4M6pKGeOUnJa6CtZ4GEaIBQvr4NZfqeu"
REDIRECT_URI = "https://oauth.pstmn.io/v1/callback"

# New authorization code from callback URL
AUTH_CODE = "5d445kackbryT_QVzUT17yIJhUrXpyWs7-npZD23rlWpFSCEudDOkR3kAQY2qbfTS5B6mdOV3wpVog8zU9Nr_XBwUAM7-OWe2iXjfNBFdTnWYwk4bZNwgq6TAX3I2yoHyq95dSjcM-zJniSAAktfoK0CCojgrRzzB-WZFeg7KXZXMI-6KC9tULYGIKNWh9aaZvfxPdN13PgFxRaVWNmGZ2nDVMbwavtdtc7TwQ*v!4371.va"

print("=" * 70)
print("🔑 TIKTOK OAUTH - EXCHANGE CODE FOR TOKEN")
print("=" * 70)
print()
print(f"Client ID: {CLIENT_ID}")
print(f"Redirect URI: {REDIRECT_URI}")
print(f"Auth Code: {AUTH_CODE[:50]}...")
print()

# Token endpoint
url = "https://open.tiktokapis.com/v2/oauth/token/"

# Request payload
data = {
    "client_key": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "code": AUTH_CODE,
    "grant_type": "authorization_code",
    "redirect_uri": REDIRECT_URI
}

print("📡 Exchanging code for access token...")

try:
    response = requests.post(url, data=data)

    print(f"📡 Status: {response.status_code}")
    print(f"📡 Response:")
    print(json.dumps(response.json(), indent=2))

    if response.status_code == 200:
        result = response.json()

        access_token = result.get('access_token')
        refresh_token = result.get('refresh_token')
        expires_in = result.get('expires_in')
        refresh_expires_in = result.get('refresh_expires_in')
        scope = result.get('scope', '')
        open_id = result.get('open_id')

        print("\n" + "=" * 70)
        print("✅ SUCCESS - TOKENS OBTAINED!")
        print("=" * 70)
        print(f"Access Token: {access_token}")
        print(f"Refresh Token: {refresh_token}")
        print(f"Open ID: {open_id}")
        print(f"Expires In: {expires_in}s ({expires_in//3600}h)")
        print(f"Refresh Expires In: {refresh_expires_in}s ({refresh_expires_in//86400}d)")
        print(f"Scopes: {scope}")
        print()

        # Save to config
        config = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "open_id": open_id,
            "expires_in": expires_in,
            "refresh_expires_in": refresh_expires_in,
            "scopes": scope,
            "status": "configured"
        }

        config_path = "config/api_credentials.json"
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)

        print(f"✅ Saved to: {config_path}")
        print()
        print("⚠️  Access token expires in 24 hours - use refresh_token after that!")

    else:
        print("\n❌ Failed to get token")
        print(f"Error: {response.text}")

except Exception as e:
    print(f"❌ Error: {e}")
