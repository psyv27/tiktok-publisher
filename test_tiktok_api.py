#!/usr/bin/env python3
"""
TikTok API Test Script
Проверка правильности TikTok API credentials

Usage:
    python3 test_tiktok_api.py
"""

import json
import sys
from pathlib import Path
from src.tiktok_api import TikTokAPIUploader

def test_api_credentials():
    """Test if API credentials are valid"""
    print("🧪 TikTok API Credentials Test")
    print("=" * 60)
    print()

    try:
        uploader = TikTokAPIUploader()
        print("✅ Config file loaded successfully")
        print(f"📂 Location: {uploader.config_path}")
        print()

        config = uploader.config
        print("📋 Configuration:")
        print(f"   Mode: {config.get('mode')}")
        print(f"   App Name: {config.get('app_name', 'N/A')}")
        print(f"   Redirect URI: {config.get('redirect_uri', 'N/A')}")

        has_client_id = bool(config.get('client_id'))
        has_client_secret = bool(config.get('client_secret'))
        has_access_token = bool(config.get('access_token'))

        print()
        print("🔑 Credentials Status:")
        print(f"   Client ID: {'✅ Present' if has_client_id else '❌ Missing'}")
        print(f"   Client Secret: {'✅ Present' if has_client_secret else '❌ Missing'}")
        print(f"   Access Token: {'✅ Present' if has_access_token else '❌ Missing'}")

        if not (has_client_id and has_client_secret and has_access_token):
            print()
            print("⚠️  Please complete credentials setup:")
            print("   1. Follow docs/TIKTOK_API_GUIDE.md")
            print("   2. Update config/api_credentials.json")
            print("   3. Run this script again")
            return False

        print()
        print("=" * 60)
        print("✅ ALL CREDENTIALS PRESENT")
        print("=" * 60)
        print()
        print("🚀 Ready to test API connection!")
        print()
        print("Next steps:")
        print("   python3 upload_to_tiktok.py <video_path> [caption] [hashtags]")
        print("=" * 60)

        return True

    except FileNotFoundError as e:
        print(f"❌ Config file not found: {e}")
        print()
        print("📋 Setup instructions:")
        print("   1. Follow docs/TIKTOK_API_GUIDE.md")
        print("   2. Get credentials from developers.tiktok.com")
        print("   3. Create config/api_credentials.json")
        return False

    except Exception as e:
        print(f"❌ Error loading config: {e}")
        return False


if __name__ == '__main__':
    success = test_api_credentials()
    sys.exit(0 if success else 1)
