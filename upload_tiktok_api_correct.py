#!/usr/bin/env python3
"""
Тест правильного TikTok Content Publishing API
Based on official documentation
"""
import os
import requests
import json

# Config
ACCESS_TOKEN = "act.NR2weFQwxe7eupnKr6ueoQCmeWgOj9R3FnpEibQDh2hRpXs4aj0KhTyclB1n!4372.va"
VIDEO_PATH = "../youtube-shorts/downloads/TikTok video #7588920065173556502.mp4"

print("=" * 70)
print("🎵 TIKTOK CONTENT PUBLISHING API")
print("=" * 70)
print()

# Проверка видео
if not os.path.exists(VIDEO_PATH):
    print(f"❌ Video not found: {VIDEO_PATH}")
    exit(1)

video_size = os.path.getsize(VIDEO_PATH)
print(f"📹 Video: {os.path.basename(VIDEO_PATH)}")
print(f"📊 Size: {video_size} bytes ({video_size/(1024*1024):.2f} MB)")
print()

# STEP 1: Проверяем creator info (как в документации)
print("📡 STEP 1: Query Creator Info...")

creator_url = "https://open.tiktokapis.com/v2/post/publish/creator_info/query/"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

creator_response = requests.post(creator_url, headers=headers, json={})

print(f"📡 Status: {creator_response.status_code}")
print(f"📡 Response: {json.dumps(creator_response.json(), indent=2)}")
print()

if creator_response.status_code != 200:
    print("❌ Cannot query creator info")
    print(f"Response: {creator_response.text}")
    exit(1)

creator_data = creator_response.json()
privacy_options = creator_data.get('data', {}).get('privacy_level_options', [])
print(f"✅ Creator info OK!")
print(f"   Privacy options: {privacy_options}")
print()

# STEP 2: Инициализируем загрузку видео
print("📡 STEP 2: Initialize Video Upload...")

init_url = "https://open.tiktokapis.com/v2/post/publish/video/init/"

init_payload = {
    "post_info": {
        "title": "API Upload Test (Private Mode)",
        "privacy_level": "SELF_ONLY",  # Unaадированные клиенты могут публиковать только privately
        "disable_duet": False,
        "disable_comment": False,
        "disable_stitch": False,
    },
    "source_info": {
        "source": "FILE_UPLOAD",
        "video_size": video_size,
        "chunk_size": video_size,  # загружаем сразу весь файл
        "total_chunk_count": 1
    }
}

init_response = requests.post(init_url, json=init_payload, headers=headers)

print(f"📡 Status: {init_response.status_code}")
print(f"📡 Response: {json.dumps(init_response.json(), indent=2)}")
print()

if init_response.status_code != 200:
    print("❌ Upload initialization failed")
    print(f"Response: {init_response.text}")
    exit(1)

# Получаем upload URL и publish_id
init_data = init_response.json()
upload_url = init_data.get('data', {}).get('upload_url')
publish_id = init_data.get('data', {}).get('publish_id')

if not upload_url or not publish_id:
    print("❌ No upload_url or publish_id returned")
    exit(1)

print(f"✅ Upload initialized!")
print(f"   Publish ID: {publish_id}")
print(f"   Upload URL: {upload_url[:80]}...")
print()

# STEP 3: Загружаем видео файл
print("📡 STEP 3: Upload Video File...")

# Вычисляем Content-Range
content_range = f"0-{video_size-1}/{video_size}"

upload_headers = {
    "Content-Type": "video/mp4",
    "Content-Range": content_range
}

print(f"📤 Uploading {video_size} bytes...")
with open(VIDEO_PATH, 'rb') as f:
    video_data = f.read()

upload_response = requests.put(upload_url, data=video_data, headers=upload_headers)

print(f"📡 Upload Status: {upload_response.status_code}")

if upload_response.status_code not in [200, 201]:
    print(f"❌ Upload failed: {upload_response.text}")
    exit(1)

print("✅ Video uploaded to TikTok CDN!")
print()

# STEP 4: Проверяем статус поста
print("📡 STEP 4: Check Post Status...")

status_url = "https://open.tiktokapis.com/v2/post/publish/status/fetch/"

status_payload = {
    "publish_id": publish_id
}

status_response = requests.post(status_url, json=status_payload, headers=headers)

print(f"📡 Status: {status_response.status_code}")
print(f"📡 Response: {json.dumps(status_response.json(), indent=2)}")
print()

print("=" * 70)
print("✅ PROCESS COMPLETE!")
print("=" * 70)
