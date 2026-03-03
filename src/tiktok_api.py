#!/usr/bin/env python3
"""
TikTok API v2 Integration
Official TikTok API for video uploading and management

Documentation: https://developers.tiktok.com/doc/video-upload/
"""

import json
import os
import hashlib
import requests
from pathlib import Path
from typing import Optional, Dict
from datetime import datetime

# TikTok API v2 Base URL
BASE_URL = "https://open.tiktokapis.com/v2"
BASE_URL_VIDEO = "https://open.tiktokapis.com/v2/"

class TikTokAPIUploader:
    """TikTok API v2 Client for video uploads"""

    def __init__(self, config_path: Optional[Path] = None):
        if config_path is None:
            config_path = Path(__file__).parent.parent / 'config' / 'api_credentials.json'

        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.session = requests.Session()

    def _load_config(self) -> Dict:
        """Load API credentials from config file"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"API credentials not found: {self.config_path}\n\n"
                                  "Please setup credentials as per docs/TIKTOK_API_GUIDE.md")

        with open(self.config_path, 'r') as f:
            return json.load(f)

    def get_access_token(self) -> str:
        """Get access token from config or generate new one"""
        return self.config.get('access_token', '')

    def _make_upload_request(self, url: str, data: Dict, files: Optional[Dict] = None) -> Dict:
        """Make authenticated request to TikTok API"""
        access_token = self.get_access_token()
        if not access_token:
            raise ValueError("No access token available. Please configure API credentials.")

        headers = {
            'Authorization': f'Bearer {access_token}',
        }

        if files:
            # For multipart/form-data requests (video upload)
            response = self.session.post(url, headers=headers, data=data, files=files)
        else:
            # For JSON requests
            response = self.session.post(url, headers=headers, json=data)

        return response.json()

    def _make_get_request(self, url: str, params: Optional[Dict] = None) -> Dict:
        """Make GET request to TikTok API"""
        access_token = self.get_access_token()
        if not access_token:
            raise ValueError("No access token available. Please configure API credentials.")

        headers = {
            'Authorization': f'Bearer {access_token}',
        }

        response = self.session.get(BASE_URL + url, headers=headers, params=params)
        return response.json()

    def get_video_upload_url(self) -> str:
        """Get video upload URL from TikTok's video_upload_url endpoint"""
        url = f"{BASE_URL}/video/upload/"
        data = {}

        try:
            response = self._make_get_request(url, params=data)

            if response.get('error', {}).get('code') != 'ok':
                error_msg = response.get('error', {}).get('message', 'Unknown error')
                raise Exception(f"TikTok API error: {response.get('error')}")

            video_url = response.get('data', {}).get('upload_url')
            if not video_url:
                raise Exception("No upload URL returned from TikTok")

            return video_url

        except Exception as e:
            print(f"❌ Failed to get upload URL: {e}")
            raise

    def upload_video_file(self, video_path: Path, upload_url: str) -> Dict:
        """Upload video file to TikTok using the upload URL"""

        if not video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")

        print(f"📤 Uploading video: {video_path}")
        print(f"📊 File size: {video_path.stat().st_size / (1024 * 1024):.2f} MB")

        try:
            with open(video_path, 'rb') as f:
                # Generate Content-MD5
                file_content = f.read()
                md5_hash = hashlib.md5(file_content).hexdigest()

                # Reset file pointer
                f.seek(0)

            # Upload to TikTok's provided upload URL
            headers = {
                'Content-Range': f'bytes 0-{len(file_content) - 1}/{len(file_content)}',
                'Content-MD5': md5_hash,
                'Content-Type': 'video/mp4',
            }

            files = {
                'video': (video_path.name, open(video_path, 'rb'), 'video/mp4')
            }

            print("🚀 Starting upload to TikTok servers...")
            response = self.session.put(upload_url, headers=headers, data=file_content)

            if response.status_code != 200 and response.status_code != 201:
                raise Exception(f"Upload failed with status {response.status_code}: {response.text}")

            print("✅ Video uploaded successfully!")

            return {
                'status': 'success',
                'upload_id': response.headers.get('Upload-Session-Id', 'unknown'),
                'response': response.json() if response.text else {}
            }

        except Exception as e:
            print(f"❌ Video upload failed: {e}")
            raise

    def publish_video(self, video_url: str, caption: str, privacy_level: str = 'public_to_everyone') -> Dict:
        """Publish video that was previously uploaded"""

        url = f"{BASE_URL}/video/publish/"

        data = {
            'post_info': {
                'title': caption,
                'privacy_level': privacy_level,
                'video_info': {
                    'file_url': video_url
                }
            }
        }

        print(f"📝 Publishing video with caption: {caption[:50]}...")

        try:
            response = self._make_upload_request(url, data)

            if response.get('error', {}).get('code') != 'ok':
                error_msg = response.get('error', {}).get('message', 'Unknown error')
                raise Exception(f"Publish failed: {error_msg}")

            publish_id = response.get('data', {}).get('publish_id')
            video_id = response.get('data', {}).get('video_id')

            print(f"✅ Video published successfully!")
            print(f"🆔 Publish ID: {publish_id}")
            print(f"🎬 Video ID: {video_id}")

            return {
                'status': 'success',
                'publish_id': publish_id,
                'video_id': video_id,
                'url': f'https://www.tiktok.com/@user/video/{video_id}' if video_id else ''
            }

        except Exception as e:
            print(f"❌ Video publish failed: {e}")
            raise

    def upload_and_publish(self, video_path: Path, caption: str,
                         privacy_level: str = 'public_to_everyone',
                         hashtags: Optional[list] = None) -> Dict:
        """Complete flow: Get URL → Upload File → Publish"""

        print("=" * 60)
        print("🎵 TikTok Video Upload Flow")
        print("=" * 60)
        print()

        try:
            # Step 1: Get upload URL
            print("📡 Step 1/3: Getting upload URL...")
            upload_url = self.get_video_upload_url()
            print(f"✅ Upload URL received")

            # Step 2: Upload video file
            print()
            print("📤 Step 2/3: Uploading video file...")
            upload_result = self.upload_video_file(video_path, upload_url)

            # Step 3: Publish video
            print()
            print("📝 Step 3/3: Publishing video...")

            # Add hashtags to caption if provided
            if hashtags:
                caption += '\n\n' + ' '.join(f'#{tag}' for tag in hashtags)

            publish_result = self.publish_video(upload_url, caption, privacy_level)

            print()
            print("=" * 60)
            print("✅ TIKTOK UPLOAD COMPLETE")
            print("=" * 60)
            print(f"🎬 Video ID: {publish_result.get('video_id')}")
            print(f"🔗 URL: {publish_result.get('url')}")
            print(f"⏰ Published at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("=" * 60)

            return publish_result

        except Exception as e:
            print()
            print("=" * 60)
            print("❌ TIKTOK UPLOAD FAILED")
            print("=" * 60)
            print(f"🔴 Error: {e}")
            print("=" * 60)
            raise


def main():
    """Test script for TikTok API"""
    TikTokAPIUploader()

if __name__ == '__main__':
    main()
