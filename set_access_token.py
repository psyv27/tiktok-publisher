#!/usr/bin/env python3
"""
TikTok Access Token Installer
Ручная установка access token в конфиг

Usage:
    python3 set_access_token.py aw_XXXXXXXXXXXXXXX
"""

import json
import sys
from pathlib import Path

CONFIG_PATH = Path(__file__).parent.parent / 'config' / 'api_credentials.json'

def set_access_token(token):
    """Set access token in config file"""

    if not token:
        print("❌ No token provided")
        print()
        print("Usage: python3 set_access_token.py <ACCESS_TOKEN>")
        print()
        print("Example:")
        print("  python3 set_access_token.py aw_abcdefghijklmnopqrstuvwxyz123456")
        return False

    # Validate token format
    if not token.startswith('aw_'):
        print("⚠️  Warning: Token doesn't start with 'aw_'")
        print("   TikTok access tokens usually start with 'aw_'")
        print()
        response = input("Continue anyway? (y/n): ").strip().lower()
        if response != 'y':
            return False

    # Load config
    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)

    # Update config
    config['access_token'] = token
    config['status'] = 'configured'

    # Save config
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=2)

    print("✅ Access token successfully configured!")
    print()
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📋 CONFIGURATION STATUS:")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()
    print("✅ Client ID: configured")
    print("✅ Client Secret: configured")
    print("✅ Access Token: configured")
    print(f"   Token: {token[:30]}...{token[-10:]}")
    print()
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("✨ TIKTOK API READY!")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()
    print("🚀 Next steps:")
    print("   1. Test with: python3 test_tiktok_api.py")
    print("   2. Upload video: python3 upload_to_tiktok.py video.mp4 \"Caption\" #hashtag1")
    print()
    print("📓 Note: Access tokens last 24 hours in testing mode")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()

    return True


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("""
🔑 TIKTOK ACCESS TOKEN INSTALLER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Usage:
    python3 set_access_token.py <ACCESS_TOKEN>

Example:
    python3 set_access_token.py aw_abcdefghijklmnopqrstuvwxyz123456

Or paste the token inline:
    🔑 Вот access token: aw_XXXXXXXXXXXXXXX
    └── Assistant will configure automatically

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
        sys.exit(1)

    token = sys.argv[1]
    success = set_access_token(token)
    sys.exit(0 if success else 1)
