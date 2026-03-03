# TikTok Video Publisher Bot

🤖 Automated TikTok video uploader using official Content Publishing API v2

## Features

- ✅ **Official TikTok API** - Content Publishing API v2 integration
- ✅ **OAuth 2.0** - Secure authentication with token refresh
- ✅ **Draft Upload** - Upload videos as drafts (manual publishing)
- ✅ **Batch Upload** - Upload all videos from directory in one script
- ✅ **Token Management** - Automated access token refresh via refresh token

## Requirements

- Python 3.8+
- [TikTok Developer Account](https://developers.tiktok.com)
- App with Content Posting API enabled
- Approved scopes: `video.upload` (for drafts) or `video.publish` (for direct publishing)

## Installation

1. **Clone repository**
```bash
git clone https://github.com/psyv27/tiktok-publisher.git
cd tiktok-publisher
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Copy config template**
```bash
cp config/api_credentials.json.example config/api_credentials.json
```

## Setup

### 1. Create TikTok App

1. Go to [TikTok Developer Portal](https://developers.tiktok.com)
2. Create a new app
3. Enable **Content Posting API** product
4. Save your `CLIENT_ID` and `CLIENT_SECRET`

### 2. Get OAuth Authorization Code

Open this URL in your browser:

```
https://www.tiktok.com/v2/auth/authorize/?client_key=YOUR_CLIENT_ID&redirect_uri=https://oauth.pstmn.io/v1/callback&response_type=code&scope=video.upload&state=123
```

**Scopes:**
- `video.upload` - For draft uploads (works with PUBLIC accounts)
- `video.publish` - For direct publishing (requires PRIVATE account if app is unaudited)

### 3. Exchange Code for Token

**Quick method:**
```bash
python3 exchange_draft_token.py
```

The script will prompt you to enter the `authorization_code` from the callback URL (the `code` parameter).

### 4. Configure Credentials

File: `config/api_credentials.json`

```json
{
  "client_id": "your_client_id",
  "client_secret": "your_client_secret",
  "redirect_uri": "https://oauth.pstmn.io/v1/callback",
  "access_token": "act...",
  "refresh_token": "rft...",
  "open_id": "-000A...",
  "expires_in": 86400,
  "refresh_expires_in": 31536000,
  "scopes": "video.upload,user.info.basic",
  "status": "configured"
}
```

## Usage

### Upload Single Video as Draft

```bash
python3 upload_as_exact.py
```

**Target file:** `../youtube-shorts/downloads/TikTok video #7588920065173556502.mp4`

Edit the script to specify your own file (change `VIDEO_PATH` variable).

### Upload All Videos from Directory

```bash
python3 upload_all_as_drafts.py
```

This script will:
- Find all `.mp4` files in `../youtube-shorts/downloads/`
- Upload each as a draft
- Show summary of successful/failed uploads

### Results

After upload:
1. Open TikTok app on your phone
2. Navigate to **Inbox / Drafts**
3. Your uploaded videos will be ready to publish

### Publish ID

Each uploaded video gets a `publish_id`, for example:
`v_inbox_file~v2.7612993423670380561`

Save this ID for tracking upload status.

## API Endpoints

### TikTok Content Publishing API v2

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v2/post/publish/inbox/video/init/` | POST | Initialize draft upload |
| `/v2/post/publish/video/init/` | POST | Initialize direct publish |
| `/v2/post/publish/status/fetch/` | POST | Check publish status |

### CDN Upload

Method: `PUT {upload_url}`

Required Headers:
```
Content-Type: video/mp4
Content-Range: bytes 0-{size-1}/{total_size}
```

Example:
```
Content-Range: bytes 0-363244/363245
```

## File Structure

```
tiktok-publisher/
├── src/                          # Core bot modules
│   ├── tiktok_bot.py            # Main TikTokBot class
│   ├── tiktok_api.py            # TikTok API client
│   ├── video_processor.py       # Video processing utilities
│   └── video_downloader.py      # YouTube downloader
├── config/                      # Configuration files
│   ├── api_credentials.json     # OAuth credentials (NOT in git!)
│   └── api_credentials.json.example  # Template
├── upload_as_exact.py           # Upload single video
├── upload_all_as_drafts.py      # Batch upload script
├── exchange_draft_token.py      # Exchange auth code for token
├── exchange_code_for_token.py   # Alternative token exchange
├── requirements.txt             # Python dependencies
├── .gitignore                   # Excludes videos, secrets, logs
└── README.md                    # This file
```

## Limitations

### Unaudited Applications

If your app hasn't passed audit yet:
- ✅ Can publish to **PRIVATE** accounts (direct publish)
- ✅ Can upload drafts to **PUBLIC** accounts
- ❌ Direct publishing to PUBLIC accounts is not allowed

### Video Requirements

- **Format:** `.mp4`, `.mov`
- **Max size:** 500 MB
- **Max duration:** 60 minutes
- **Recommended aspect ratio:** 9:16 (vertical video)

## Troubleshooting

### 416 Range Not Satisfiable

**Problem:** Incorrect Content-Range header format

**Solution:** Use exact format:
```
Content-Range: bytes 0-{size-1}/{total_size}
```

Example: For 363245 bytes:
```
Content-Range: bytes 0-363244/363245
```

### unaudited_client_can_only_post_to_private_accounts

**Problem:** Trying to publish directly to public account

**Solution:**
- Use `video.upload` scope for draft uploads
- OR make your TikTok account private

### Access Token Expired

**Problem:** Access token only valid for 24 hours

**Solution:** Use refresh_token to get a new access_token
```python
# Or re-run auth flow
python3 exchange_draft_token.py
```

## Security

- ❌ **NOT** commit `config/api_credentials.json` to git repository
- ❌ **NOT** share access_token or refresh_token with anyone
- ✅ Use `.env` files for sensitive data
- ✅ Store credentials securely (password managers, encrypted storage)

## Deployment

### Install via Cron

```bash
# Edit crontab
crontab -e

# Add this line (runs every 6 hours)
0 */6 * * * cd /path/to/tiktok-publisher && /usr/bin/python3 upload_all_as_drafts.py >> bot.log 2>&1
```

### Docker (Optional)

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "upload_all_as_drafts.py"]
```

Build and run:
```bash
docker build -t tiktok-publisher .
docker run -v $(pwd)/config:/app/config tiktok-publisher
```

## API References

- [TikTok Content Posting API](https://developers.tiktok.com/doc/content-posting-api-get-started)
- [TikTok Scopes Overview](https://developers.tiktok.com/doc/scopes-overview)
- [TikTok App Audit](https://developers.tiktok.com/application/content-posting-api)
- [Content Guidelines](https://developers.tiktok.com/doc/content-sharing-guidelines)

## OAuth Flow

### Authorization Endpoint

```
GET https://www.tiktok.com/v2/auth/authorize/
```

Parameters:
- `client_key` - Your CLIENT_ID
- `redirect_uri` - https://oauth.pstmn.io/v1/callback
- `response_type` - code
- `scope` - video.upload,user.info.basic
- `state` - Any string (e.g., "123")

### Token Exchange Endpoint

```
POST https://open.tiktokapis.com/v2/oauth/token/
```

Body:
```json
{
  "client_key": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET",
  "code": "AUTHORIZATION_CODE",
  "grant_type": "authorization_code",
  "redirect_uri": "https://oauth.pstmn.io/v1/callback"
}
```

Example Response:
```json
{
  "access_token": "act...",
  "token_type": "Bearer",
  "expires_in": 86400,
  "refresh_token": "rft...",
  "refresh_expires_in": 31536000,
  "scope": "video.upload,user.info.basic",
  "open_id": "-000A..."
}
```

## License

MIT

## Contributing

PRs are welcome! Please ensure:
- Code follows PEP 8 style guidelines
- All tests pass
- Documentation is updated

## Support

- Issues: [GitHub Issues](https://github.com/psyv27/tiktok-publisher/issues)
- TikTok Developer Docs: https://developers.tiktok.com

---

**Built for automated TikTok video publishing** 🚀
