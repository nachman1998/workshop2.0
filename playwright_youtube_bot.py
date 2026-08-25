import random

from playwright.sync_api import sync_playwright
import time
import argparse
import random



def yt(HAR_name):
    with (sync_playwright() as p):
        # Channel can be "chrome", "msedge", "chrome-beta", "msedge-beta" or "msedge-dev".
        browser = p.chromium.launch(channel="chrome",
                                    headless=False,
                                    args=['--disable-blink-features=AutomationControlled']
        )

        context = browser.new_context(
            user_agent= 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
            java_script_enabled=True,
            viewport={"width": 1280, "height": 720},
            device_scale_factor= 1,
            record_har_path=HAR_name
        )
        # Navigate YouTube video and wait for the page's
        # `load` event before continuing.
        page = context.new_page()
        page.goto("https://www.youtube.com/watch?v=7bOptq-NPJQ",wait_until="load")

        # Open the player's settings
        setting = page.locator(".ytp-settings-button")
        # Wait a random interval to avoid perfectly regular/robotic timing between clicks.
        page.wait_for_timeout(1000 + abs(random.gauss(0, 1000)))
        setting.hover()
        page.wait_for_timeout(10 + abs(random.gauss(0, 100)))
        setting.click()
        # In the settings menu, hover then click the "Quality" option to
        # open the quality submenu.
        Q = page.get_by_text("Quality").nth(0)
        page.wait_for_timeout(1000 + abs(random.gauss(0, 1000)))
        Q.hover()
        page.wait_for_timeout(10 + abs(random.gauss(0, 100)))
        Q.click()
        # In the quality submenu, hover then click the "1080p" option to
        # switch playback resolution up to 1080p.
        Q7 = page.get_by_text("1080p")
        page.wait_for_timeout(1000 + abs(random.gauss(0, 1000)))
        Q7.hover()
        page.wait_for_timeout(10 + abs(random.gauss(0, 100)))
        Q7.click()
        st_time = time.time()
        # Play for about 31 seconds, repeatedly check
        # the play/pause button's to see if video is playing
        while time.time() - st_time < 31:
            play=page.locator("button[class='ytp-play-button ytp-button']")
            if play.get_attribute("data-title-no-tooltip")=="Play":
                play.hover()
                play.click()
                time.sleep(0.1)

        box = page.locator("button[class='ytp-play-button ytp-button']").bounding_box()
        page.mouse.move(
            box["x"] + box["width"] / 2 + random.randint(0, 2),
            box["y"] + box["height"] / 2 + random.randint(1, 2),
            steps=10
        )
        print(page.locator("div[class='ytp-progress-bar']").get_attribute("aria-valuetext"))
        print(page.title())
        page.close()
        context.close()
        browser.close()



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--output_name', required=True, )# Output path for the HAR file to be recorded during this session.
    args = parser.parse_args()
    yt(args.output_name)
