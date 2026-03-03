#!/usr/bin/env python3
"""
Main pipeline: Download → Process → Upload to TikTok
"""
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from video_downloader import download_video
from video_processor import process_for_tiktok, split_into_clips
from tiktok_bot import TikTokBot

# Settings
DEFAULT_HASHTAGS = ["#fyp", "#viral", "#trending"]
DEFAULT_PRIVACY = "public"
DEFAULT_HEADLESS = False  # First run: show browser for login

def process_and_upload(url_or_path, caption="", hashtags=None, privacy=DEFAULT_PRIVACY, headless=False):
    """
    Full pipeline: download, process, upload to TikTok

    Args:
        url_or_path: Video URL or local file path
        caption: Video caption text
        hashtags: List of hashtags (default: #fyp #viral #trending)
        privacy: Privacy status (public/friends/private)
        headless: Run browser headless (after first login)
    """
    # Download if URL
    if url_or_path.startswith(('http://', 'https://')):
        print(f"\n🌐 Downloading from: {url_or_path}")
        video_path = download_video(url_or_path)
        if not video_path:
            print("❌ Download failed")
            return False
    else:
        print(f"\n📁 Processing file: {url_or_path}")
        video_path = url_or_path
        if not os.path.exists(video_path):
            print(f"❌ File not found: {video_path}")
            return False

    # Process for TikTok
    print(f"\n🔪 Processing for TikTok...")
    processed = process_for_tiktok(video_path)

    if not processed:
        print("❌ Processing failed")
        return False

    # Upload
    bot = TikTokBot(headless=headless)

    print(f"\n📤 Uploading {len(processed)} video(s) to TikTok...")

    success_count = 0
    for i, video in enumerate(processed):
        print(f"\n[{i+1}/{len(processed)}] {os.path.basename(video)}")

        try:
            bot.upload_video(
                video,
                caption=caption,
                hashtags=hashtags,
                headless=headless
            )
            success_count += 1
            print(f"✅ Upload complete")
        except Exception as e:
            print(f"❌ Upload failed: {e}")

    print(f"\n" + "="*50)
    print(f"📊 SUMMARY")
    print("="*50)
    print(f"   Videos processed: {len(processed)}")
    print(f"   Successfully uploaded: {success_count}")
    print(f"   Failed: {len(processed) - success_count}")
    print("="*50)

    return success_count > 0

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 pipeline.py <url_or_path> [caption] [hashtags] [privacy] [headless]")
        print("\nExamples:")
        print("  # URL with default settings")
        print("  python3 pipeline.py https://youtube.com/watch?v=xxx \"Cool video\"")
        print("\n  # File with custom hashtags (comma-separated)")
        print("  python3 pipeline.py ../video.mp4 \"My Caption\" \"#fyp #viral\"")
        print("\n  # Headless mode (after first login)")
        print("  python3 pipeline.py ../video.mp4 \"Test\" \"#test\" public true")
        print("\n💡 First run: headless=False (shows browser for login)")
        print("   Subsequent runs: headless=True (uses saved cookies)")
        sys.exit(1)

    url_or_path = sys.argv[1]
    caption = sys.argv[2] if len(sys.argv) > 2 else ""
    hashtags_arg = sys.argv[3] if len(sys.argv) > 3 else ""
    privacy = sys.argv[4] if len(sys.argv) > 4 else DEFAULT_PRIVACY
    headless = False if len(sys.argv) < 6 else sys.argv[5].lower() == 'true'

    # Parse hashtags
    hashtags = hashtags_arg.split() if hashtags_arg else None

    process_and_upload(url_or_path, caption, hashtags, privacy, headless)
