#!/usr/bin/env python3
"""
Upload draft with exact Content-Range format
"""
import os
import requests
import json

# Load config
with open("config/api_credentials.json") as f:
    config = json.load(f)

ACCESS_TOKEN = config['access_token']
VIDEO_PATH = "../youtube-shorts/downloads/TikTok video #7588920065173556502.mp4"

print("=" * 70)
print("🎵 TIKTOK DRAFT UPLOAD - EXACT CONTENT-RANGE")
print("=" * 70)

video_size = os.path.getsize(VIDEO_PATH)
print(f"📊 Video size: {video_size} bytes ({video_size/(1024*1024):.2f} MB)")

# STEP 1: Init upload
print("\n📡 Step 1: Initialize...")

init_url = "https://open.tiktokapis.com/v2/post/publish/inbox/video/init/"

headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}

payload = {
    "source_info": {
        "source": "FILE_UPLOAD",
        "video_size": video_size,
        "chunk_size": video_size,
        "total_chunk_count": 1
    }
}

response = requests.post(init_url, json=payload, headers=headers)
print(f"Status: {response.status_code}")

if response.status_code != 200:
    print(f"❌ Init failed: {response.text}")
    exit(1)

result = response.json()
upload_url = result['data']['upload_url']
publish_id = result['data']['publish_id']

print(f"✅ Publish ID: {publish_id}")
print(f"Upload URL: {upload_url[:100]}...")

# STEP 2: Upload with exact Content-Range
print("\n📡 Step 2: Upload video...")

with open(VIDEO_PATH, 'rb') as f:
    video_data = f.read()

# Exact format: Content-Range: bytes <start>-<end>/<total>
content_range = f"bytes 0-{video_size-1}/{video_size}"

upload_headers = {
    "Content-Type": "video/mp4",
    "Content-Range": content_range
}

print(f"📋 Content-Range: {content_range}")
print(f"📤 Uploading {len(video_data)} bytes...")

upload_response = requests.put(upload_url, data=video_data, headers=upload_headers)

print(f"\n📡 Upload Status: {upload_response.status_code}")
print(f"📡 Response: {upload_response.text}")

if upload_response.status_code in [200, 201]:
    print("\n✅ UPLOAD SUCCESSFUL!")
    print(f"📌 Publish ID: {publish_id}")
    print(f"📱 Check TikTok app - video in drafts/inbox")
else:
    print(f"\n❌ Upload failed with status {upload_response.status_code}")
