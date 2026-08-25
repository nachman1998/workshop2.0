import argparse
import random
import time

from playwright.sync_api import sync_playwright, TimeoutError


def play(HAR_name):
    with sync_playwright() as p:
        # bundled Chromium, in visible (non-headless) mode, with a flag
        # to reduce the browser's automation fingerprint
        # presumably to make the traffic look more like genuine human
        browser = p.chromium.launch(
            channel="chrome",
            headless=False,
            args=["--disable-blink-features=AutomationControlled"],
        )
        # Create a new browsing context with a realistic computer
        # Chrome user-agent string, JS enabled, a standard 1280x720
        # viewport, and HAR recording turned on
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
            java_script_enabled=True,
            viewport={"width": 1280, "height": 720},
            device_scale_factor=1,
            record_har_path=HAR_name,
        )

        page = context.new_page()
        cdp = context.new_cdp_session(page)
        cdp.send("Network.enable")
        cdp.send("Network.setCacheDisabled", {"cacheDisabled": True})
        # Navigate to the target SoundCloud share link and wait for the
        # page's `load` event before continuing.
        page.goto(
        "https://on.soundcloud.com/rakZPRfwxJ0xotFC24",
            wait_until="load",
        )
        # Click  cookie button when it appears
        try:
            cooki_butten=page.locator("#onetrust-accept-btn-handler")
            cooki_butten.wait_for(state="visible")
            while cooki_butten.is_visible():
                cooki_butten.click()
                page.wait_for_timeout(500)
            print("Clicked 'Reject all'")
        except TimeoutError:
            print("'Reject all' button not found")
        # run for approximately 31 seconds
        st_time = time.time()
        while time.time() - st_time < 31:
            print(time.time() - st_time)
            # Wait a random interval to avoid perfectly regular/robotic timing between checks.
            page.wait_for_timeout(abs(random.gauss(1000, 10)))

            # Check for and dismiss close button
            try:
                close_butten=page.locator("button.modal__closeButton")
                close_butten.wait_for(state="visible")
                while close_butten.is_visible():
                    close_butten.click()
                    page.wait_for_timeout(500)
                print("Clicked close button")
            except TimeoutError:
                print("Close button not found")
            # Try to click the main "Play" button. This is attempted
            try:
                page.locator('a.sc-button-play.playButton.sc-button.sc-button-xxlarge[title="Play"]').wait_for(
                    state="visible", timeout=100)

                page.locator('a.sc-button-play.playButton.sc-button.sc-button-xxlarge[title="Play"]').click()
                print("Clicked play button")
            except TimeoutError:
                print("play button not found")


        page.close()
        context.close()
        browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--output_name', required=True, )# Output path for the HAR file to be recorded during this session.
    args = parser.parse_args()
    play(args.output_name)