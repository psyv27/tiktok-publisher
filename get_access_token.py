#!/usr/bin/env python3
"""
TikTok OAuth 2.0 Authorization Flow Script
Generates TikTok API Access Token using Client Credentials

This script implements the OAuth 2.0 authorization flow for TikTok API
"""

import json
import base64
import hashlib
import urllib.parse
import secrets
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
import threading

# TikTok OAuth endpoints
AUTH_BASE_URL = "https://www.tiktok.com/v2/auth"
TOKEN_URL = f"{AUTH_BASE_URL}/token"


def load_config():
    """Load API credentials"""
    config_path = Path(__file__).parent.parent / 'config' / 'api_credentials.json'
    with open(config_path, 'r') as f:
        return json.load(f)


def save_access_token(access_token):
    """Save access token to config"""
    config_path = Path(__file__).parent.parent / 'config' / 'api_credentials.json'
    with open(config_path, 'r') as f:
        config = json.load(f)

    config['access_token'] = access_token
    config['status'] = 'configured'

    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)

    print(f"✅ Access token saved to: {config_path}")


def get_auth_url(config):
    """Generate OAuth authorization URL"""
    client_id = config['client_id']
    redirect_uri = config['redirect_uri']
    scopes = config['scopes']

    # Generate state parameter for CSRF protection
    state = secrets.token_urlsafe(16)

    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'response_type': 'code',
        'scope': ','.join(scopes),
        'state': state
    }

    auth_url = f"{AUTH_BASE_URL}/authorize?{urllib.parse.urlencode(params)}"

    return auth_url, state


class CallbackHandler(BaseHTTPRequestHandler):
    """Handle OAuth callback"""

    state_expected = None
    auth_code = None

    def do_GET(self):
        """Handle GET request to callback endpoint"""

        if self.path.startswith('/callback'):
            query = urllib.parse.parse_qs(self.path.split('?')[1])

            # Verify state parameter
            state_received = query.get('state', [None])[0]
            if state_received != CallbackHandler.state_expected:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Invalid state parameter')
                return

            # Get authorization code
            code = query.get('code', [None])[0]
            if code:
                CallbackHandler.auth_code = code
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                response_html = """
                <html>
                <head><title>TikTok OAuth Callback</title></head>
                <body>
                <h1>✅ Authorization Successful</h1>
                <p>Your authorization code has been captured.</p>
                <p>You can close this window.</p>
                </body>
                </html>
                """
                self.wfile.write(response_html.encode())
                print("✅ Authorization code received from TikTok")
            else:
                # Handle error
                error = query.get('error', ['Unknown error'])[0]
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                response_html = f"""
                <html>
                <head><title>TikTok OAuth Error</title></head>
                <body>
                <h1>❌ Authorization Failed</h1>
                <p>Error: {error}</p>
                </body>
                </html>
                """
                self.wfile.write(response_html.encode())
                print(f"❌ Authorization error: {error}")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

    def log_message(self, format, *args):
        """Suppress default logging"""
        pass


def exchange_code_for_token(auth_code, config):
    """Exchange authorization code for access token"""

    client_id = config['client_id']
    client_secret = config['client_secret']
    redirect_uri = config['redirect_uri']

    # Prepare token request
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    # Prepare payload - use Authorization Code Flow
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': auth_code,
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri
    }

    print("🔄 Exchanging authorization code for access token...")

    response = requests.post(TOKEN_URL, headers=headers, data=data)
    response_data = response.json()

    if 'access_token' in response_data:
        access_token = response_data['access_token']
        print("✅ Access token received successfully!")
        return access_token
    else:
        print("❌ Failed to get access token")
        print(f"Response: {response_data}")

        if 'error_description' in response_data:
            print(f"Error: {response_data['error_description']}")

        raise Exception(f"Token exchange failed: {response_data}")


def run_oauth_flow():
    """Run complete OAuth 2.0 authorization flow"""

    print("=" * 70)
    print("🎵 TIKTOK OAUTH 2.0 AUTHORIZATION")
    print("=" * 70)
    print()

    # Load config
    config = load_config()
    print(f"✅ Config loaded for app: {config.get('app_name', 'Unknown')}")
    print()

    # Generate authorization URL
    print("📡 Generating authorization URL...")
    auth_url, state = get_auth_url(config)

    # Start callback server on localhost:3000
    print("🚀 Starting callback server on http://localhost:3000")
    CallbackHandler.state_expected = state

    server_address = ('0.0.0.0', 3000)
    httpd = HTTPServer(server_address, CallbackHandler)
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    print("✅ Callback server running...")
    print()

    # Display auth URL and instructions
    print("=" * 70)
    print("🔐 AUTHORIZATION REQUIRED")
    print("=" * 70)
    print()
    print("📱 TikTok authorization URL:")
    print(auth_url)
    print()
    print("⚠️  NEXT STEPS:")
    print("   1. Copy and paste the authorization URL into your browser")
    print("   2. Allow the application to access your TikTok account")
    print("   3. You will be redirected to http://localhost:3000/callback")
    print("   4. The script will automatically capture the authorization code")
    print()
    print("💡 TIPS:")
    print("   • Make sure ports 3000 are available")
    print("   • Use the same redirect URI configured in TikTok Developer Portal")
    print("   • The script will continue automatically after authorization")
    print("=" * 70)
    print()

    # Wait for callback (with timeout)
    print("⏳ Waiting for authorization code...")
    print("   (This will happen automatically after TikTok redirects)")
    print()

    timeout = 300  # 5 minutes timeout
    callback_received = False

    for i in range(timeout):
        if CallbackHandler.auth_code:
            callback_received = True
            break
        if i == 10:  # After 10 seconds
            print("   ⏰ Still waiting... (check your browser after completing authorization)")
        time.sleep(1)

    # Stop server
    httpd.shutdown()
    httpd.server_close()
    server_thread.join()
    print("✅ Callback server stopped")
    print()

    if not callback_received:
        print()
        print("=" * 70)
        print("❌ TIMEOUT")
        print("=" * 70)
        print()
        print("⚠️  Authorization timed out after 5 minutes")
        print()
        print("📋 What went wrong:")
        print("   • URL might not have been opened properly")
        print("   • Authorization might have been denied")
        print("   • Redirect callback might not have reached localhost:3000")
        print()
        print("💡 Try again:")
        print("   1. Check network connectivity")
        print("   2. Ensure you can reach http://localhost:3000")
        print("   3. Verify redirect URI matches TikTok app settings")
        print("=" * 70)
        return False

    # Exchange code for token
    try:
        print("=" * 70)
        print("🔄 EXCHANGING CODE FOR TOKEN")
        print("=" * 70)
        print()

        access_token = exchange_code_for_token(CallbackHandler.auth_code, config)

        print()
        print("=" * 70)
        print("✅ AUTHORIZATION COMPLETE")
        print("=" * 70)
        print()
        print(f"🔑 Access Token: {access_token[:20]}...")
        print(f"📂 Token saved to config file")
        print()
        print("✨ TikTok API is now ready to use!")
        print("=" * 70)

        # Save access token
        save_access_token(access_token)

        return True

    except Exception as e:
        print()
        print("=" * 70)
        print("❌ TOKEN EXCHANGE FAILED")
        print("=" * 70)
        print()
        print(f"🔴 Error: {e}")
        print()
        print("💡 Troubleshooting:")
        print("   • Check if Client ID and Secret are correct")
        print("   • Ensure Redirect URI matches app settings")
        print("   • Try re-running the authorization flow")
        print("=" * 70)
        return False


def main():
    """Main entry point"""
    import time
    import requests  # Import here to check if requests is available

    try:
        success = run_oauth_flow()
        return 0 if success else 1

    except KeyboardInterrupt:
        print("\n⚠️  Authorization cancelled by user")
        return 1

    except Exception as e:
        print(f"\n❌ Authorization failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(main())
