#!/usr/bin/env python3
"""
TikTok video uploader using Playwright (automation)
"""
import os
import time
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '../config.json')
COOKIES_PATH = os.path.join(os.path.dirname(__file__), '../cookies.json')

class TikTokBotUploader:
    """TikTok video uploader using Playwright (automation)"""
    def __init__(self, headless=True):
        self.config = self.load_config()
        self.headless = headless
        self.browser = None
        self.context = None
        self.page = None

    def init_browser(self, headless=True):
        """Initialize browser for use outside of upload_video method"""
        from playwright.sync_api import sync_playwright

        p = sync_playwright().start()

        # Launch browser
        self.browser = p.chromium.launch(headless=headless)

        # Create context
        self.context = self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            locale='en-US',
            timezone_id='America/New_York',
        )

        # Load cookies if available
        if self.load_cookies(self.context):
            print("✅ Existing cookies loaded")

        # Create page
        self.page = self.context.new_page()

        # Navigate to TikTok to test connection
        self.page.goto('https://www.tiktok.com/upload', wait_until='networkidle', timeout=60000)

        return True

    def load_config(self):
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)

    def save_cookies(self, browser):
        """Save cookies for future sessions"""
        cookies = browser.contexts[0].cookies()
        with open(COOKIES_PATH, 'w') as f:
            json.dump(cookies, f)
        print("✅ Cookies saved")

    def load_cookies(self, context):
        """Load cookies if available"""
        if os.path.exists(COOKIES_PATH):
            cookies = json.loads(open(COOKIES_PATH).read())
            context.add_cookies(cookies)
            print("✅ Cookies loaded")
            return True
        return False

    def upload_video(self, video_path, caption="", hashtags=None, headless=False, privacy='public'):
        """
        Upload video to TikTok
        """
        if hashtags is None:
            hashtags = self.config['hashtags']['default']

        # Combine caption with hashtags
        full_caption = caption
        if hashtags:
            tags_str = ' '.join(hashtags)
            full_caption = f"{caption}\n\n{tags_str}"

        video_path = os.path.abspath(video_path)

        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video not found: {video_path}")

        print(f"📤 Uploading to TikTok: {os.path.basename(video_path)}")
        print(f"   Caption: {full_caption[:50]}...")

        with sync_playwright() as p:
            # Launch browser - for TikTok, may need non-headless first for auth
            browser = p.chromium.launch(headless=headless)
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
                locale='en-US',
                timezone_id='America/New_York',
            )

            # Load cookies if available
            has_cookies = self.load_cookies(context)

            page = context.new_page()

            try:
                # Navigate to TikTok upload page
                print("🌐 Opening TikTok...")
                page.goto('https://www.tiktok.com/upload', wait_until='networkidle', timeout=60000)

                # Check if logged in
                if not has_cookies or page.locator('//button[contains(text(), "Log in")]').count() > 0:
                    print("⚠️  Not logged in. Please login manually...")

                    if headless:
                        print("🔓 Switching to headed mode to login...")
                        browser.close()
                        return self.upload_video(video_path, caption, hashtags, headless=False)

                # Wait for upload area
                print("📤 Looking for upload button...")
                upload_selectors = [
                    'input[type="file"]',
                    'input[accept*="video"]',
                    '[data-e2e="upload-input"]',
                ]

                upload_input = None
                for selector in upload_selectors:
                    try:
                        page.wait_for_selector(selector, timeout=5000)
                        upload_input = page.locator(selector).first
                        print(f"✅ Found upload input with selector: {selector}")
                        break
                    except:
                        continue

                if not upload_input:
                    raise Exception("Could not find file upload input - TikTok UI may have changed")

                # Upload video
                print("\n📁 Uploading video file...")
                upload_input.set_input_files(video_path)

                # Wait for upload to complete (check for upload progress or success indicators)
                print("⏳ Waiting for TikTok to process the video...")
                time.sleep(5)

                # Check for success indicators of upload completion
                upload_success_indicators = [
                    'text=/video uploaded/i',
                    'text=/upload complete/i',
                    '[data-e2e="upload-progress"] >> text=/100%/i',
                ]

                for indicator in upload_success_indicators:
                    try:
                        page.wait_for_selector(indicator, timeout=10000)
                        print(f"✅ Upload complete indicator found: {indicator}")
                        break
                    except:
                        pass

                # Additional wait to ensure TikTok has processed the video
                print("⏳ Waiting additional time for video processing...")
                for i in range(15):
                    time.sleep(1)
                    print(f"   Processing: {i+1}/15 seconds")

                # Add caption - try multiple selectors
                caption_selectors = [
                    '[contenteditable="true"] >> near=span:has-text("Describe your video")',
                    '[contenteditable="true"] >> near=span:has-text("#")',
                    'textarea[placeholder*="Describe"]',
                    'textarea[placeholder*="caption"]',
                    '[contenteditable="true"] >> nth=0',  # First editable element
                ]

                caption_input = None
                for selector in caption_selectors:
                    try:
                        page.wait_for_selector(selector, timeout=5000)
                        caption_input = page.locator(selector).first
                        print(f"✅ Found caption input with selector: {selector}")
                        break
                    except:
                        continue

                if caption_input:
                    caption_input.fill(full_caption)
                    print(f"✅ Caption added: {full_caption[:50]}...")
                else:
                    print("⚠️  Could not find caption input, but video is uploaded")

                # Set privacy if needed
                privacy = self.config['upload']['privacy']
                if privacy != 'public':
                    privacy_btn = page.locator('[role="button"] >> near=span:has-text("Who can watch")')
                    if privacy_btn.count() > 0:
                        privacy_btn.click()
                        time.sleep(1)
                        # Select privacy option
                        option = page.locator(f'[role="menuitem"] >> text={privacy.title()}')
                        if option.count() > 0:
                            option.click()

                # Post video
                print("\n📝 Posting video...")
                # Try multiple selectors for Post button (TikTok UI may change)
                post_selectors = [
                    'button >> text=/Post/i',
                    'button:has-text("Post")',
                    '[data-e2e="post-button"]',
                    'button[type="submit"]',
                    'button:has-text("Publish")',
                ]

                post_btn = None
                for selector in post_selectors:
                    try:
                        page.wait_for_selector(selector, timeout=5000)
                        post_btn = page.locator(selector).first
                        print(f"✅ Found Post button with selector: {selector}")
                        break
                    except:
                        continue

                if not post_btn:
                    raise Exception("Could not find Post/Post button - TikTok UI may have changed")

                # Wait for button to be enabled and clickable
                post_btn.wait_for(state='visible', timeout=10000)
                time.sleep(2)  # Wait for any processing

                # Scroll into view to ensure it's clickable
                post_btn.scroll_into_view_if_needed()
                time.sleep(1)

                # Click the button
                post_btn.click()

                # Wait for success indicators
                print("⏳ Waiting for posting confirmation...")
                time.sleep(5)

                # Check for success indicators or error messages
                success_indicators = [
                    'text=/posted/i',
                    'text=/Your video is posted/i',
                    '[data-e2e="modal"] >> text=/posted/i',
                ]

                posted = False
                for indicator in success_indicators:
                    try:
                        page.wait_for_selector(indicator, timeout=5000)
                        posted = True
                        print(f"✅ Found success indicator: {indicator}")
                        break
                    except:
                        continue

                if posted or page.locator('button >> text=/Post/i').count() == 0:
                    print("✅ Video posted successfully (button disappeared)!")
                else:
                    print("⚠️  Upload may have completed or is in review")

            except Exception as e:
                print(f"❌ Upload failed: {e}")
                print("\n💡 Tips:")
                print("   - Check if cookies are saved properly")
                print("   - Try running with headless=False for debugging")
                print("   - Make sure TikTok didn't change upload UI")
                raise

            finally:
                # Save cookies if not already saved
                if not has_cookies:
                    self.save_cookies(browser)

                browser.close()

        return True

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python3 tiktok_uploader.py <video_path> [caption] [hashtags]")
        print("\nExamples:")
        print("  python3 tiktok_uploader.py ../video.mp4 \"My cool video\" \"#fyp #viral\"")
        print("\nFirst run will open browser - login to TikTok and it will save cookies")
        sys.exit(1)

    video_path = sys.argv[1]
    caption = sys.argv[2] if len(sys.argv) > 2 else ""
    hashtags_arg = sys.argv[3] if len(sys.argv) > 3 else ""

    hashtags = hashtags_arg.split() if hashtags_arg else None

    bot = TikTokBot()
    try:
        bot.upload_video(video_path, caption, hashtags, headless=False)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
