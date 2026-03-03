#!/usr/bin/env python3
"""
TikTok OAuth Playground Guide
Руководство по получению access token через TikTok OAuth Playground
"""

print("""
🎵 TIKTOK OAUTH PLAYGROUND SETUP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 Easy Method: TikTok provides an OAuth Playground where you
   can generate access tokens manually without coding!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 STEPS TO GENERATE ACCESS TOKEN:

🔹 STEP 1: OAuth Playground Setup
────────────────────────────────
1. Go to: https://developers.tiktok.com/oauth/playground/

2. Fill in the form:
   • Client ID: sbaws49sqt018swoyo  (✅ Already configured)
   • Client Secret: 4M6pKGeOUnJa6CtZ4GEaIBQvr4NZfqeu  (✅ Already configured)
   • Redirect URI: http://localhost:3000/callback

🔹 STEP 2: Authorize
────────────────────────────────
1. Click the "Get Access Token" or "Authorize" button

2. Login with your TikTok account when prompted

3. Allow the application permissions:
   ✓ video.list
   ✓ video.create
   ✓ video.publish

4. After authorization, you'll receive an access token

🔹 STEP 3: Copy Access Token
────────────────────────────────
1. Look for the "Access Token" section on the page

2. Copy the token (starts with something like "aw_...")

3. Send me the token using this format:
   
   🔑 Вот access token: aw_XXXXXXXXXXXXXXXXXX...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚙️  CONFIGURATION STATUS:

Status: Partially Configured ✅
Client ID: ✅ Present (sbaws49sqt018swoyo)
Client Secret: ✅ Present (4M6pKGeOUnJa6CtZ4GEaIBQvr4NZfqeu)
Access Token: ❌ MISSING (needs to be generated)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 ALTERNATIVE: OAuth Flow Script

If you prefer, you can run the automated OAuth flow:
    python3 get_access_token.py

This script will:
1) Start a local web server on port 3000
2) Generate an authorization URL
3) Capture the callback automatically
4) Exchange code for access token
5) Save token to config file

⚠️  Note: This method requires ability to run HTTP server

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 TROUBLESHOOTING:

Problem: OAuth Playground doesn't work?
Solution: Try using TikTok's Developer Console instead

Problem: Token expired?
Solution: Access tokens last 24 hours in testing mode. For production, implement refresh tokens.

Problem: Wrong permissions?
Solution: Ensure your app has the correct scopes: video.list, video.create, video.publish

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✨ READY WHEN YOU ARE!

After getting the access token from OAuth Playground,
just paste it here and I'll configure the system!

Example:
🔑 Вот access token: aw_abcdefghijklmnopqrstuvwxyz123456

Then:
- TikTok upload API will work
- Testing can begin
- Integration ready to go!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

""")
