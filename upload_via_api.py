#!/usr/bin/env python3
"""
TikTok Video Upload using Official API v2
"""
import os
import requests
import json

# Конфигурация
CONFIG_PATH = "config/api_credentials.json"
BASE_URL = "https://open.tiktokapis.com/v2/"

def load_config():
    """Load API credentials from config file"""
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)

def upload_video_init(video_path, access_token):
    """
    Шаг 1: Инициализация загрузки - получаем upload_url
    Используем правильный endpoint для direct publishing
    """
    url = f"{BASE_URL}direct_video/upload/init/"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    data = {
        "video_size": os.path.getsize(video_path)
    }

    response = requests.post(url, headers=headers, json=data)

    print(f"📡 Upload Init Status: {response.status_code}")
    print(f"📡 Response: {response.text[:200]}...")

    if response.status_code == 200:
        result = response.json()
        print("✅ Upload initialized!")
        print(f"   Upload URL: {result.get('data', {}).get('upload_url', '')[:50]}...")
        return result
    else:
        print(f"❌ Upload init failed: {response.text}")
        return None

def upload_video_file(video_path, upload_url):
    """
    Шаг 2: Загрузка файла на TikTok CDN
    """
    print(f"\n📁 Uploading video file of size {os.path.getsize(video_path) / (1024*1024):.2f} MB...")

    headers = {
        "Content-Type": "video/mp4"
    }

    with open(video_path, 'rb') as f:
        response = requests.put(upload_url, data=f, headers=headers)

    print(f"📡 File Upload Status: {response.status_code}")

    if response.status_code in [200, 201]:
        print("✅ Video file uploaded successfully!")
        return True
    else:
        print(f"❌ File upload failed: {response.text}")
        return False

def publish_video(access_token, video_id, caption="Test video #viral #fyp"):
    """
    Шаг 3: Публикация видео - Direct Publish endpoint
    """
    url = f"{BASE_URL}direct_video/publish/"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    data = {
        "video_id": video_id,
        "caption": caption
    }

    print(f"\n📝 Publishing video with caption: {caption[:50]}...")
    response = requests.post(url, headers=headers, json=data)

    print(f"📡 Publish Status: {response.status_code}")
    result = response.json()

    if response.status_code == 200:
        print("✅ Video published successfully!")
        print(f"   Share URL: {result.get('data', {}).get('share_url', 'N/A')}")
        return result
    else:
        print(f"❌ Publish failed: {json.dumps(result, indent=2)}")
        return None

def upload_video(video_path, caption="Test video"):
    """
    Полный процесс загрузки видео
    """
    print("=" * 70)
    print("🎵 TIKTOK VIDEO UPLOAD (OFFICIAL API v2)")
    print("=" * 70)
    print()

    # Загрузка конфигурации
    config = load_config()
    access_token = config.get('access_token')

    print(f"🔑 Access Token: {access_token[:30]}...")
    print(f"📹 Video: {video_path}")
    print(f"📊 Size: {os.path.getsize(video_path) / (1024*1024):.2f} MB")
    print()

    # Шаг 1: Инициализация загрузки
    init_result = upload_video_init(video_path, access_token)

    if not init_result:
        return False

    upload_url = init_result.get('data', {}).get('upload_url', '')
    if not upload_url:
        print("❌ No upload URL received")
        return False

    # Шаг 2: Загрузка файла
    if not upload_video_file(video_path, upload_url):
        return False

    # Ожидание обработки видео на серверах TikTok
    print("⏳ Waiting for TikTok to process video...")
    import time
    time.sleep(3)

    # Шаг 3: Публикация
    publish_result = publish_video(
        access_token,
        video_id="",  # Может быть получен из init_response
        caption=caption
    )

    if publish_result:
        print("\n" + "=" * 70)
        print("✅ UPLOAD COMPLETE!")
        print("=" * 70)
        return True
    else:
        print("\n" + "=" * 70)
        print("❌ UPLOAD FAILED")
        print("=" * 70)
        return False

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python3 upload_via_api.py <video_path> [caption]")
        sys.exit(1)

    video_path = sys.argv[1]
    caption = sys.argv[2] if len(sys.argv) > 2 else "Test upload #viral #fyp"

    if not os.path.exists(video_path):
        print(f"❌ Video file not found: {video_path}")
        sys.exit(1)

    upload_video(video_path, caption)
