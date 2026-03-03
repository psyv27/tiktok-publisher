#!/usr/bin/env python3
"""
Upload video as DRAFT using video.upload scope (inbox method)
Endpoint: /v2/post/publish/inbox/video/init/
"""
import os
import requests
import json
import time

# Load config
with open("config/api_credentials.json") as f:
    config = json.load(f)

ACCESS_TOKEN = config['access_token']
VIDEO_PATH = "../youtube-shorts/downloads/TikTok video #7588920065173556502.mp4"

print("=" * 70)
print("🎵 TIKTOK UPLOAD - DRAFT模式 (INBOX VIDEO INIT)")
print("=" * 70)
print()
print(f"🔑 Token: {ACCESS_TOKEN[:30]}...")
print(f"📹 Video: {VIDEO_PATH}")
print()

# Check video
if not os.path.exists(VIDEO_PATH):
    print(f"❌ Video not found: {VIDEO_PATH}")
    exit(1)

video_size = os.path.getsize(VIDEO_PATH)
print(f"📊 Size: {video_size} bytes ({video_size/(1024*1024):.2f} MB)")

# Use chunked upload (100KB chunks)
CHUNK_SIZE = 100 * 1024  # 100KB
total_chunks = (video_size + CHUNK_SIZE - 1) // CHUNK_SIZE
print(f"📦 Will upload in {total_chunks} chunks of {CHUNK_SIZE/1024}KB each")

# ============================================================================
# STEP 1: Initialize Inbox Video Upload
# ============================================================================
print("\n📡 STEP 1: Initialize Inbox Video Upload...")

url = "https://open.tiktokapis.com/v2/post/publish/inbox/video/init/"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# Source: FILE_UPLOAD (loading file from disk)
payload = {
    "source_info": {
        "source": "FILE_UPLOAD",
        "video_size": video_size,
        "chunk_size": video_size,  # Upload as single chunk
        "total_chunk_count": 1
    }
}

print(f"🔗 URL: {url}")
print(f"📦 Payload: {json.dumps(payload, indent=2)}")

try:
    response = requests.post(url, json=payload, headers=headers)

    print(f"\n📡 Status: {response.status_code}")
    result = response.json()
    print(f"📡 Response:")
    print(json.dumps(result, indent=2))

    if response.status_code != 200 or result.get('error', {}).get('code') != 'ok':
        print("\n❌ Initialization failed")
        exit(1)

    # Extract data
    publish_id = result['data']['publish_id']
    upload_url = result['data']['upload_url']

    print(f"\n✅ SUCCESS!")
    print(f"   Publish ID: {publish_id}")
    print(f"   Upload URL: {upload_url[:80]}...")

    print(f"\n⏰ Note: Upload URL expires in 1 hour")

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# ============================================================================
# STEP 2: Upload Video File (try multiple methods)
# ============================================================================
print("\n📡 STEP 2: Upload Video File to TikTok...")

# Try Method 1: PUT with basic headers
print(f"📤 Trying Method 1: PUT with basic headers...")

upload_headers = {
    "Content-Type": "video/mp4",
    "Content-Length": str(video_size)
}

try:
    with open(VIDEO_PATH, 'rb') as f:
        video_data = f.read()

    upload_response = requests.put(upload_url, data=video_data, headers=upload_headers)

    print(f"📡 Upload Status: {upload_response.status_code}")
    print(f"📡 Response: {upload_response.text[:200]}...")

    if upload_response.status_code in [200, 201]:
        print("✅ Video uploaded successfully to TikTok CDN!")
    else:
        # Try Method 2: PUT without Content-Length (auto-calculated)
        print(f"\n📤 Trying Method 2: PUT without Content-Length...")

        upload_headers = {"Content-Type": "video/mp4"}
        upload_response = requests.put(upload_url, data=video_data, headers=upload_headers)

        print(f"📡 Upload Status: {upload_response.status_code}")
        print(f"📡 Response: {upload_response.text[:200]}...")

        if upload_response.status_code in [200, 201]:
            print("✅ Video uploaded successfully to TikTok CDN!")
        else:
            # Try Method 3: POST with multipart/form-data
            print(f"\n📤 Trying Method 3: POST with multipart/form-data...")

            files = {
                'video': (os.path.basename(VIDEO_PATH), video_data, 'video/mp4')
            }

            upload_response = requests.post(upload_url, files=files)

            print(f"📡 Upload Status: {upload_response.status_code}")
            print(f"📡 Response: {upload_response.text[:200]}...")

            if upload_response.status_code in [200, 201]:
                print("✅ Video uploaded successfully to TikTok CDN!")
            else:
                print("\n❌ All upload methods failed")
                print(f"\n⏰ Possible issue: Upload URL expired (1 hour limit)")
                exit(1)

except Exception as e:
    print(f"❌ Upload error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# ============================================================================
# STEP 3: Check Status (Optional - drafts go to inbox immediately)
# ============================================================================
print("\n📡 STEP 3: Check Publish Status...")

status_url = "https://open.tiktokapis.com/v2/post/publish/status/fetch/"

status_payload = {
    "publish_id": publish_id
}

try:
    time.sleep(2)  # Small delay for processing
    status_response = requests.post(status_url, json=status_payload, headers=headers)

    print(f"📡 Status: {status_response.status_code}")
    if status_response.status_code == 200:
        status_result = status_response.json()
        print(f"📡 Response:")
        print(json.dumps(status_result, indent=2))
except:
    print("⚠️  Status check skipped (may need more time)")

# ============================================================================
# SUCCESS
# ============================================================================
print("\n" + "=" * 70)
print("✅ DRAFT UPLOAD COMPLETE!")
print("=" * 70)
print(f"\n📌 Publish ID: {publish_id}")
print(f"\n📱 Next Steps:")
print(f"   1. Open TikTok app on your device")
print(f"   2. Check your Inbox/Saved for this draft")
print(f"   3. Edit the draft and publish it")
print(f"\n🎯 Video uploaded successfully as DRAFT!")
