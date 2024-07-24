from playwright.sync_api import sync_playwright
from requests.cookies import RequestsCookieJar
import time
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
# Replace with your Hemmings login credentials
EMAIL = config["LOGIN"]["email"]
PASSWORD = config["LOGIN"]["password"]


def get_cookies():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Navigate to the Hemmings login page
        page.goto("https://www.hemmings.com/auctions/account/sign-in",
                  wait_until='load', timeout=60000)

        # Fill in the email and password fields and submit
        page.fill("input[name='email']", EMAIL)
        page.fill("input[name='password']", PASSWORD)
        page.click("button[type='submit']")
        time.sleep(5)
        # Wait for navigation to complete
        page.wait_for_load_state('networkidle')

        # Extract cookies from the browser context
        cookies = context.cookies()

        # Close browser
        browser.close()

        # Convert Playwright cookies to RequestsCookieJar
        cookie_jar = RequestsCookieJar()
        for cookie in cookies:
            cookie_jar.set(cookie['name'], cookie['value'],
                           domain=cookie['domain'], path=cookie['path'])

        return cookie_jar


if __name__ == "__main__":
    cookies = get_cookies()
    print(cookies)
