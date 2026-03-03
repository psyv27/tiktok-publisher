#!/usr/bin/env python3
"""
TikTok Video Upload using Official API v2 (Corrected)
Рабочая загрузка через TikTok API
"""
import os
import requests
import json
import time

# Конфигурация
CONFIG_PATH = "config/api_credentials.json"

def load_config():
    """Load API credentials from config file"""
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)

def get_upload_url(access_token, video_size):
    """
    Получить upload URL от TikTok
    """
    url = "https://open.tiktokapis.com/v2/video/upload/"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    data = {
        "video_size": video_size
    }

    print("🔑 Requesting upload URL...")
    response = requests.post(url, headers=headers, json=data)

    print(f"📡 Status: {response.status_code}")
    print(f"📡 Response: {response.text[:500]}...")

    if response.status_code == 200:
        result = response.json()
        if result.get('data', {}).get('upload_url'):
            print("✅ Got upload URL!")
            return result
    else:
        print(f"❌ Failed: {response.text}")

    return None

def upload_to_s3(upload_url, video_path):
    """
    Загрузить видео на TikTok CDN (S3-like)
    """
    print(f"\n📁 Uploading video ({os.path.getsize(video_path) / (1024*1024):.2f} MB)...")

    with open(video_path, 'rb') as f:
        response = requests.put(upload_url, data=f)

    print(f"📡 Upload status: {response.status_code}")

    if response.status_code in [200, 201]:
        print("✅ Video uploaded successfully!")
        return True
    else:
        print(f"❌ Upload failed: {response.text}")
        return False

def publish_video(access_token, video_id, caption="Test video #viral #fyp"):
    """
    Публикация видео (если нужно)
    Note: Для some endpoints публикация автоматическая
    """
    print(f"\n📝 Publishing video...")

    # Попробуем разные publish endpoints
    publish_urls = [
        "https://open.tiktokapis.com/v2/video/publish/",
        "https://open.tiktokapis.com/v2/direct_video/publish/",
    ]

    for url in publish_urls:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        data = {
            "video_id": video_id,
            "caption": caption
        }

        print(f"📡 Trying: {url}")
        response = requests.post(url, headers=headers, json=data)

        print(f"   Status: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print("✅ Video published!")
            print(f"   Share URL: {result.get('data', {}).get('share_url', 'N/A')}")
            return result
        else:
            print(f"   Response: {response.text[:200]}...")

    return None

def main():
    """Main upload function"""
    print("=" * 70)
    print("🎵 TIKTOK VIDEO UPLOAD (OFFICIAL API)")
    print("=" * 70)
    print()

    video_path = "../youtube-shorts/downloads/TikTok video #7588920065173556502.mp4"
    caption = "Test upload from API #viral #fyp #bot #test"

    # Проверка файла
    if not os.path.exists(video_path):
        print(f"❌ Video not found: {video_path}")
        return

    # Загрузка конфига
    config = load_config()
    access_token = config.get('access_token')

    print(f"🔑 Token: {access_token[:30]}...")
    print(f"📹 Video: {os.path.basename(video_path)}")
    print(f"📊 Size: {os.path.getsize(video_path) / (1024*1024):.2f} MB")
    print()

    # Шаг 1: Get upload URL
    init_result = get_upload_url(access_token, os.path.getsize(video_path))

    if not init_result:
        print("❌ Cannot get upload URL")
        print("\n💡 Possible issues:")
        print("   - Access token expired (24hr lifetime)")
        print("   - App not authorized for video.publish scope")
        print("   - Token lacks required permissions")

        # Проверим валидность токена
        print("\n🔍 Testing access token validity...")
        test_url = "https://open.tiktokapis.com/v2/user/info/"
        test_headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        test_response = requests.get(test_url, headers=test_headers)

        if test_response.status_code == 200:
            print("✅ Token is valid for user.info.basic scope")
            print(f"   User info: {json.dumps(test_response.json(), indent=2)}")

            # Проверить scope
            if 'video.publish' in access_token:

                print("⚠️  Token has video.publish scope but upload endpoint failing")
            else:

                print("❌ Token may not have video.publish scope")
        else:
            print(f"❌ Token invalid: {test_response.text}")

        return

    upload_url = init_result.get('data', {}).get('upload_url')
    video_id = init_result.get('data', {}).get('video_id')

    # Шаг 2: Upload video file
    if not upload_to_s3(upload_url, video_path):
        return

    # Шаг 3: Publish
    print("⏳ Waiting for processing...")
    time.sleep(5)

    if video_id:
        publish_video(access_token, video_id, caption)
    else:
        print("⚠️  No video_id from init, may need to publish separately")
    print("\n🎉 Process complete!")

if __name__ == "__main__":
    main()
