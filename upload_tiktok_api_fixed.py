#!/usr/bin/env python3
"""
Working TikTok Video Upload via Official Content Posting API
Based on TikTok Content Posting API documentation
"""
import os
import requests
import json
import time

def upload_video_simple(video_path, caption="Test video"):
    """Simple upload to TikTok Content Publishing API"""

    # API Config
    config = {
        "access_token": "act.NR2weFQwxe7eupnKr6ueoQCmeWgOj9R3FnpEibQDh2hRpXs4aj0KhTyclB1n!4372.va",
        "client_id": "sbaws49sqt018swoyo",
    }

    print("=" * 70)
    print("🎵 TIKTOK CONTENT PUBLISHING API - VIDEO UPLOAD")
    print("=" * 70)
    print()

    # Check video
    if not os.path.exists(video_path):
        print(f"❌ Video not found: {video_path}")
        return False

    video_size = os.path.getsize(video_path)
    print(f"📹 Video: {os.path.basename(video_path)}")
    print(f"📊 Size: {video_size / (1024*1024):.2f} MB")
    print(f"🎫 Caption: {caption}")
    print()

    # STEP 1: Get publish URL and upload URL
    print("📡 STEP 1: Getting upload URLs...")

    # TikTok Content Publishing API endpoint
    url = "https://open.tiktokapis.com/v2/post/publish/inbox/video/init/"

    payload = {
        "video_byte_size": video_size,
        "video_width": 1080,
        "video_height": 1920,
    }

    headers = {
        "Authorization": f"Bearer {config['access_token']}",
        "Content-Type": "application/json"
    }

    print(f"🔗 Endpoint: {url}")
    print(f"📦 Payload: {json.dumps(payload, indent=2)}")

    response = requests.post(url, json=payload, headers=headers)

    print(f"\n📡 Response Status: {response.status_code}")
    print(f"📡 Response Body:")
    print(json.dumps(response.json(), indent=2))

    if response.status_code != 200:
        print(f"\n❌ FAILED: {response.status_code}")
        return False

    data = response.json()
    publish_url = data.get('data', {}).get('publish_url')
    upload_url = data.get('data', {}).get('upload_url')
    video_id = data.get('data', {}).get('video_id')

    print(f"\n✅ SUCCESS!")
    print(f"   Publish URL: {publish_url[:50]}...")
    print(f"   Upload URL: {upload_url[:50]}...")
    print(f"   Video ID: {video_id}")

    if not upload_url or not publish_url:
        print("❌ Missing URLs in response")
        return False

    # STEP 2: Upload video file
    print("\n📡 STEP 2: Uploading video file...")

    video_headers = {
        "Content-Type": "video/mp4",
        "Content-Range": f"0-{video_size-1}/{video_size}"
    }

    print(f"🔗 Upload URL: {upload_url[:100]}...")

    with open(video_path, 'rb') as video_file:
        upload_response = requests.put(upload_url, data=video_file, headers=video_headers)

    print(f"\n📡 Upload Status: {upload_response.status_code}")

    if upload_response.status_code not in [200, 201]:
        print(f"❌ Upload failed: {upload_response.text}")
        return False

    print("✅ Video uploaded successfully!")

    # STEP 3: Create post
    print("\n📡 STEP 3: Creating post...")

    post_config = {
        "post_info": {
            "title": "Video Upload",
            "description": caption
        },
        "source_info": {
            "source": "PULL_FROM_URL",
            "video_url": None,
            "photo_urls": [],
            "cover_image_url": None,
        },
        "post_media": {
            "media_type": "VIDEO",
            "video_url": upload_url,
        },
        "publish_time": 0,
        "disable_comment": False,
        "disable_duet": False,
        "disable_stitch": False,
    }

    post_headers = {
        "Authorization": f"Bearer {config['access_token']}",
        "Content-Type": "application/json"
    }

    print(f"🔗 Publish URL: {publish_url[:100]}...")
    print(f"📦 Post Config: {json.dumps(post_config, indent=2)}")

    post_response = requests.post(publish_url, json=post_config, headers=post_headers)

    print(f"\n📡 Publish Status: {post_response.status_code}")
    print(f"📡 Response Body:")
    print(json.dumps(post_response.json(), indent=2))

    if post_response.status_code in [200, 201]:
        print("\n" + "=" * 70)
        print("✅ UPLOAD COMPLETE!")
        print("=" * 70)
        return True
    else:
        print("\n" + "=" * 70)
        print("❌ PUBLISH FAILED")
        print("=" * 70)
        return False

if __name__ == "__main__":
    video_path = "../youtube-shorts/downloads/TikTok video #7588920065173556502.mp4"
    caption = "Test upload via Content Publishing API #viral #fyp #bot"

    upload_video_simple(video_path, caption)
