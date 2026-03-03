#!/usr/bin/env python3
"""
Video downloader using yt-dlp
Supports: YouTube, TikTok, Instagram, Twitter, etc.
"""
import os
import subprocess
import sys
from pathlib import Path

DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), '../downloads')

def download_video(url, output_dir=None):
    """
    Download video from URL
    Returns path to downloaded file
    """
    if output_dir is None:
        output_dir = DOWNLOAD_DIR

    os.makedirs(output_dir, exist_ok=True)

    print(f"📥 Downloading from: {url}")

    cmd = [
        'yt-dlp',
        '-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        '--merge-output-format', 'mp4',
        '-o', os.path.join(output_dir, '%(title)s.%(ext)s'),
        '--no-playlist',
        url
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        # Find downloaded file from output
        output_lines = result.stdout.split('\n')
        for line in output_lines:
            if '[download] Destination:' in line:
                video_path = line.split('[download] Destination:')[-1].strip()
                print(f"✅ Downloaded: {video_path}")
                return video_path

        # Alternative: find newest mp4 in dir
        mp4_files = list(Path(output_dir).glob('*.mp4'))
        if mp4_files:
            video_path = str(max(mp4_files, key=os.path.getctime))
            print(f"✅ Downloaded: {video_path}")
            return video_path

        print("❌ Could not find downloaded file")
        return None

    except subprocess.CalledProcessError as e:
        print(f"❌ Download failed: {e}")
        print(f"   {e.stderr}")
        return None

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 video_downloader.py <URL>")
        print("Example: python3 video_downloader.py https://youtube.com/watch?v=xxx")
        sys.exit(1)

    url = sys.argv[1]
    download_video(url)
