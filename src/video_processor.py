#!/usr/bin/env python3
"""
Video processor: resize to TikTok format (9:16, max 60s)
"""
import os
import subprocess
import math
from pathlib import Path

INPUT_DIR = os.path.join(os.path.dirname(__file__), '../downloads')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '../uploads')

# TikTok requirements
MAX_DURATION = 60  # seconds
TARGET_WIDTH = 1080
TARGET_HEIGHT = 1920  # 9:16
PREFERRED_ASPECT_RATIO = 9/16

def get_video_info(video_path):
    """Get video duration, resolution, and aspect ratio"""
    cmd = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height,duration',
        '-of', 'json',
        video_path
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    import json

    data = json.loads(result.stdout)
    stream = data['streams'][0]

    return {
        'width': int(stream['width']),
        'height': int(stream['height']),
        'duration': float(stream['duration']),
        'aspect_ratio': int(stream['width']) / int(stream['height'])
    }

def process_for_tiktok(video_path, output_name=None):
    """
    Process video for TikTok upload:
    1. Resize to 9:16 (1080x1920)
    2. Crop/pad accordingly
    3. Trim to max 60s if needed
    4. Optional: split into multiple clips if >60s

    Returns:
        List of paths to processed videos
    """
    video_path = os.path.abspath(video_path)

    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video not found: {video_path}")

    print(f"\n📹 Processing: {os.path.basename(video_path)}")

    # Get video info
    info = get_video_info(video_path)
    print(f"   Original: {info['width']}×{info['height']}, {info['duration']:.1f}s, AR={info['aspect_ratio']:.2f}")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    outputs = []

    # Check if video is longer than 60s
    if info['duration'] > MAX_DURATION:
        print(f"⚠️  Video ({info['duration']:.1f}s) exceeds TikTok limit ({MAX_DURATION}s)" )
        print(f"   Option 1: Trim to 60s")
        print(f"   Option 2: Split into multiple clips")

        # First, create a 60s version
        output_60s = os.path.join(OUTPUT_DIR, 'tiktok_60s.mp4')
        process_single(
            video_path,
            output_60s,
            start_time=0,
            duration=MAX_DURATION,
            target_width=TARGET_WIDTH,
            target_height=TARGET_HEIGHT
        )
        outputs.append(output_60s)
        print(f"   ✅ Created 60s version")

        # Offer to split
        clip_count = math.ceil(info['duration'] / MAX_DURATION)
        print(f"\n   💡 Can split into {clip_count} clips of {MAX_DURATION}s each")
        print(f"   Run: python3 src/video_processor.py {video_path} split")

    else:
        # Short enough, just resize
        if output_name is None:
            output_name = f'tiktok_{os.path.splitext(os.path.basename(video_path))[0]}.mp4'

        output_path = os.path.join(OUTPUT_DIR, output_name)

        process_single(
            video_path,
            output_path,
            start_time=0,
            duration=info['duration'],
            target_width=TARGET_WIDTH,
            target_height=TARGET_HEIGHT
        )
        outputs.append(output_path)
        print(f"   ✅ Resized to 9:16")

    return outputs

def process_single(input_path, output_path, start_time=0, duration=None,
                   target_width=1080, target_height=1920):
    """
    Process single video clip
    """
    cmd = [
        'ffmpeg',
        '-i', input_path,
        '-ss', str(start_time),
    ]

    if duration is not None:
        cmd.extend(['-t', str(duration)])

    # Scale to target dimensions (maintain aspect ratio)
    # Then crop to exact target size
    scale_filter = f'scale={target_width}:{target_height}:force_original_aspect_ratio=increase'
    crop_filter = f'crop={target_width}:{target_height}'

    cmd.extend([
        '-vf', f'{scale_filter},{crop_filter}',
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-preset', 'fast',
        '-y',  # Overwrite
        output_path
    ])

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"❌ FFmpeg error: {result.stderr}")
        raise RuntimeError(f"FFmpeg failed: {result.stderr}")

    return output_path

def split_into_clips(video_path, clip_duration=60):
    """
    Split long video into multiple clips for TikTok
    """
    info = get_video_info(video_path)
    total_duration = info['duration']
    num_clips = math.ceil(total_duration / clip_duration)

    print(f"\n🔪 Splitting into {num_clips} clips of {clip_duration}s each")

    output_dir = os.path.join(OUTPUT_DIR, 'clips')
    os.makedirs(output_dir, exist_ok=True)

    outputs = []

    for i in range(num_clips):
        start_time = i * clip_duration
        if start_time >= total_duration:
            break

        # Last clip might be shorter
        if start_time + clip_duration > total_duration:
            duration = total_duration - start_time
        else:
            duration = clip_duration

        output_path = os.path.join(output_dir, f'clip_{i+1}.mp4')

        print(f"\n   Clip {i+1}/{num_clips}: {start_time}s -> {start_time+duration:.1f}s")

        process_single(
            video_path,
            output_path,
            start_time=start_time,
            duration=duration,
            target_width=TARGET_WIDTH,
            target_height=TARGET_HEIGHT
        )

        outputs.append(output_path)
        print(f"   ✅ Created: {os.path.basename(output_path)}")

    return outputs

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python3 video_processor.py <video_path> [mode]")
        print("\nModes:")
        print("  resize  - Just resize to 9:16 (default)")
        print("  split   - Split video into 60s clips")
        print("\nExamples:")
        print("  python3 video_processor.py ../video.mp4")
        print("  python3 video_processor.py ../video.mp4 split")
        sys.exit(1)

    video_path = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else 'resize'

    if mode == 'split':
        try:
            outputs = split_into_clips(video_path)
            print(f"\n✓ Created {len(outputs)} clips")
        except Exception as e:
            print(f"❌ Split failed: {e}")
    else:
        try:
            outputs = process_for_tiktok(video_path)
            print(f"\n✓ Created {len(outputs)} TikTok-ready video(s)")
            for out in outputs:
                print(f"   → {out}")
        except Exception as e:
            print(f"❌ Processing failed: {e}")
