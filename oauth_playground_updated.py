#!/usr/bin/env python3
"""

TikTok OAuth Playground Instructions (Updated!)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔑 UPDATED: Redirect URI changed to Postman callback URL

✅ New Redirect URI: https://oauth.pstmn.io/v1/callback

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 UPDATED STEPS:

🔹 STEP 1: OAuth Playground
──────────────────────────────────────────────────────────
1. Go to: https://developers.tiktok.com/oauth/playground/

2. Fill in the form:
   • Client ID: sbaws49sqt018swoyo
   • Client Secret: 4M6pKGeOUnJa6CtZ4GEaIBQvr4NZfqeu
   • Redirect URI: https://oauth.pstmn.io/v1/callback   ← NEW!

🔹 STEP 2: Authorize
──────────────────────────────────────────────────────────
1. Click "Authorize" or "Get Access Token"

2. Login with TikTok

3. Allow permissions: video.create, video.publish, video.list

4. Get your access token

🔹 STEP 3: Copy Access Token
──────────────────────────────────────────────────────────
Copy the access token and send to me in this format:

🔑 Вот access token: aw_XXXXXXXXXXXXXXX

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 WHAT CHANGED:

BEFORE: http://localhost:3000/callback
AFTER:  https://oauth.pstmn.io/v1/callback

REASON: TikTok doesn't allow localhost for redirect in
        production apps. Postman URL is a public callback.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 ALTERNATIVE: If Postman URL doesn't work, try:

Options:
1. Use your own domain if you have one
2. Create a page on a VPS/webhosting
3. Use https://example.com/callback (if your app allows)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ CONFIG UPDATED! Ready for OAuth Playground!

Try now with the new Redirect URI!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""

print(__doc__)
