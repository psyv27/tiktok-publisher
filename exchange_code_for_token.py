#!/usr/bin/env python3
"""
Exchange TikTok OAuth code for access token
"""
import requests
import json
from urllib.parse import unquote

# Конфигурация
CLIENT_ID = "sbaws49sqt018swoyo"
CLIENT_SECRET = "4M6pKGeOUnJa6CtZ4GEaIBQvr4NZfqeu"
REDIRECT_URI = "https://oauth.pstmn.io/v1/callback"

# Декодируем code из callback URL
callback_url = "https://oauth.pstmn.io/v1/callback?code=bPMxkiw__pbVxB9PUvJ7-rBks0uWNrgp4s8SrTRnaAYQyg2l6NBEbKPMnNQH_Ry06cNT-XKrzoYc8GRDuivgE6-O46TgywJHxFHa060uFxdBL7B8iyQF6WIkR515AHAmJuDIgFoJSKOYE8IYDlm146oeEcl3O8AQuy15TpCRHXxerZh5nkG3DB6dzmHmxPBr0B7HUK6y7IEeugewnCUBQE_RTh7QQdSWTtpCjg%2Av%214423.va&scopes=user.info.basic%2Cvideo.publish&state=123"

# Извлекаем code
import re
code_match = re.search(r'code=([^&]+)', callback_url)
if code_match:
    AUTH_CODE = unquote(code_match.group(1))
    print(f"✅ Extracted auth code: {AUTH_CODE[:50]}...")
else:
    print("❌ Could not extract code from URL")
    exit(1)

# Обмен code на access token
print("\n🔄 Exchanging authorization code for access token...")

token_url = "https://open.tiktokapis.com/v2/oauth/token/"

data = {
    "client_key": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "code": AUTH_CODE,
    "grant_type": "authorization_code",
    "redirect_uri": REDIRECT_URI
}

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
}

response = requests.post(token_url, data=data, headers=headers)

print(f"📡 Response status: {response.status_code}")

if response.status_code == 200:
    token_data = response.json()
    print("\n✅ SUCCESS! Token received:")
    print(json.dumps(token_data, indent=2))

    # Сохраняем в конфиг
    config_path = "config/api_credentials.json"

    with open(config_path, 'r') as f:
        config = json.load(f)

    config['access_token'] = token_data.get('access_token', '')
    config['refresh_token'] = token_data.get('refresh_token', '')
    config['token_expires_at'] = token_data.get('expires_in', '')
    config['status'] = 'configured'
    config['last_updated'] = '2026-03-03'

    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)

    print(f"\n✅ Tokens saved to {config_path}")
    print(f"   Access Token: {token_data.get('access_token', '')[:30]}...")
    print(f"   Refresh Token: {token_data.get('refresh_token', '')[:30]}...")

else:
    print(f"\n❌ Token exchange failed!")
    print(f"Response: {response.text}")
    exit(1)
