import random

from playwright.sync_api import sync_playwright
import time
import argparse

from trio import sleep

def wiki(HAR_name):
    with sync_playwright() as p:
        # Channel can be "chrome", "msedge", "chrome-beta", "msedge-beta" or "msedge-dev".

        # bundled Chromium, in visible (non-headless) mode, with a flag
        # to reduce the browser's automation fingerprint
        # presumably to make the traffic look more like genuine human
        browser = p.chromium.launch(channel="chrome",
                                    headless=False,
                                    args=['--disable-blink-features=AutomationControlled']
        )
        # Create a new browsing context with a realistic computer
        # Chrome user-agent string, JS enabled, a standard 1280x720
        # viewport, and HAR recording turned on
        context = browser.new_context(
            user_agent= 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
            java_script_enabled=True,
            viewport={"width": 1280, "height": 720},
            device_scale_factor= 1,
            record_har_path=HAR_name
        )

        page = context.new_page()
        # Navigate to the starting article 'Artificial intelligence' and wait
        page.goto("https://en.wikipedia.org/wiki/Artificial_intelligence",wait_until="networkidle")
        # hop 1 to article "computational systems"
        link = page.get_by_role("link", name="computational systems").first
        # Wait a random interval to avoid perfectly regular/robotic timing between clicks.
        page.wait_for_timeout(4000 + (random.gauss(0, 1000)))
        link.click()
        # hop 2 to article "machine"
        link = page.get_by_role("link", name="machine").first
        page.wait_for_timeout(4000 + (random.gauss(0, 1000)))
        link.click()
        # hop 3 to article "thermodynamic system"
        link = page.get_by_role("link", name="thermodynamic system").first
        page.wait_for_timeout(4000 + (random.gauss(0, 1000)))
        link.click()
        page.wait_for_timeout(4000 + (random.gauss(0, 1000)))
        page.close()
        context.close()
        browser.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--output_name', required=True, )# Output path for the HAR file to be recorded during this session.
    args = parser.parse_args()
    wiki(args.output_name)