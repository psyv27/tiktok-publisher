#!/usr/bin/env python3
"""
Upload all videos from youtube-shorts/downloads/ as TikTok drafts
"""
import os
import requests
import json
import glob

# Load config
with open("config/api_credentials.json") as f:
    config = json.load(f)

ACCESS_TOKEN = config['access_token']
VIDEO_DIR = "../youtube-shorts/downloads/"

def upload_as_draft(video_path):
    """Upload single video as draft"""

    if not os.path.exists(video_path):
        return None, f"❌ Not found: {video_path}"

    video_size = os.path.getsize(video_path)
    filename = os.path.basename(video_path)

    print(f"\n{'='*70}")
    print(f"📹 Uploading: {filename}")
    print(f"📊 Size: {video_size} bytes ({video_size/(1024*1024):.2f} MB)")
    print(f"{'='*70}")

    # Step 1: Init upload
    init_url = "https://open.tiktokapis.com/v2/post/publish/inbox/video/init/"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "source_info": {
            "source": "FILE_UPLOAD",
            "video_size": video_size,
            "chunk_size": video_size,
            "total_chunk_count": 1
        }
    }

    try:
        response = requests.post(init_url, json=payload, headers=headers)

        if response.status_code != 200:
            return None, f"❌ Init failed: {response.status_code} - {response.text}"

        result = response.json()
        upload_url = result['data']['upload_url']
        publish_id = result['data']['publish_id']

        print(f"✅ Init success - Publish ID: {publish_id}")

        # Step 2: Upload video
        with open(video_path, 'rb') as f:
            video_data = f.read()

        content_range = f"bytes 0-{video_size-1}/{video_size}"

        upload_headers = {
            "Content-Type": "video/mp4",
            "Content-Range": content_range
        }

        print(f"📤 Uploading...")

        upload_response = requests.put(upload_url, data=video_data, headers=upload_headers)

        if upload_response.status_code not in [200, 201]:
            return None, f"❌ Upload failed: {upload_response.status_code} - {upload_response.text}"

        print(f"✅ Upload complete (status {upload_response.status_code})")

        return publish_id, None

    except Exception as e:
        return None, f"❌ Error: {e}"


print("=" * 70)
print("🎵 TIKTOK DRAFT UPLOADER - ALL VIDEOS")
print("=" * 70)

# Find all video files
video_files = glob.glob(os.path.join(VIDEO_DIR, "*.mp4"))

if not video_files:
    print(f"\n❌ No video files found in: {VIDEO_DIR}")
    exit(1)

print(f"\n📁 Found {len(video_files)} video files")
print(f"📂 Directory: {VIDEO_DIR}\n")

# Upload all videos
successful = []
failed = []

for idx, video_path in enumerate(video_files, 1):
    print(f"\n[ {idx}/{len(video_files)} ] Processing...")
    print(f"📂 Path: {video_path}")

    publish_id, error = upload_as_draft(video_path)

    if publish_id:
        successful.append({
            'file': os.path.basename(video_path),
            'publish_id': publish_id,
            'path': video_path
        })
    else:
        failed.append({
            'file': os.path.basename(video_path),
            'error': error
        })

# Summary
print("\n" + "=" * 70)
print("📊 UPLOAD SUMMARY")
print("=" * 70)
print(f"✅ Successful: {len(successful)}/{len(video_files)}")
print(f"❌ Failed: {len(failed)}/{len(video_files)}")

if successful:
    print("\n✅ UPLOADED VIDEOS:")
    for item in successful:
        print(f"   📹 {item['file']}")
        print(f"      Publish ID: {item['publish_id']}")
        print(f"      Path: {item['path']}")

if failed:
    print("\n❌ FAILED UPLOADS:")
    for item in failed:
        print(f"   📹 {item['file']}")
        print(f"      Error: {item['error']}")

print("\n" + "=" * 70)
print(f"📱 Check TikTok app - videos in drafts/inbox")
print("=" * 70)
