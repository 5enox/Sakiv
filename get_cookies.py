# from playwright.sync_api import sync_playwright
# from requests.cookies import RequestsCookieJar
# import time
# import configparser

# config = configparser.ConfigParser()
# config.read("config.ini")
# # Replace with your Hemmings login credentials
# EMAIL = config["LOGIN"]["email"]
# PASSWORD = config["LOGIN"]["password"]


# def get_cookies():
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         context = browser.new_context()
#         page = context.new_page()

#         # Navigate to the Hemmings login page
#         page.goto("https://www.hemmings.com/auctions/account/sign-in",
#                   wait_until='load', timeout=60000)

#         # Fill in the email and password fields and submit
#         page.fill("input[name='email']", EMAIL)
#         page.fill("input[name='password']", PASSWORD)
#         page.click("button[type='submit']")
#         time.sleep(5)

#         def log_request(request):
#             if request.resource_type in ['xhr', 'fetch']:
#                 if request.url == 'https://www.hemmings.com/stories-api/landing/featured-vehicles':
#                     print("Login request intercepted")
#                     print(f'Headers are :', request.headers['Cookie'])

#                     # Listen to network requests
#         page.on("request", log_request)
#         # Wait for navigation to complete
#         page.goto("https://www.hemmings.com/",
#                   wait_until='load', timeout=60000)
#         page.wait_for_load_state('networkidle')

#         # Extract cookies from the browser context
#         cookies = context.cookies()

#         # Close browser
#         browser.close()

#         # Convert Playwright cookies to RequestsCookieJar
#         cookie_jar = RequestsCookieJar()
#         for cookie in cookies:
#             cookie_jar.set(cookie['name'], cookie['value'],
#                            domain=cookie['domain'], path=cookie['path'])

#         return cookie_jar


# if __name__ == "__main__":
#     cookies = get_cookies()
#     print(cookies)


import requests

# The provided cookie string
cookie_string = ("OptanonConsent=groups%3DC0004%3A0; visid_incap_2011533=/oIGRmwESOOOCHCTcLiH++BVnmYAAAAAQkIPAAAAAAC8jmZkX2dOepDP9CkIjeRE; "
                 "visid_incap_984766=OtrnOEBeSxet7Hf9Y+1afhlanmYAAAAAQkIPAAAAAACA8Ny1AcRA2okPhMp8A0itk/fqO8WbXPFy; "
                 "nlbi_984766=0um0M2KRgTNTTyukoeynngAAAAAvd6uzKc4PUOOV8G2IWPKV; "
                 "incap_ses_250_984766=6tF3K2bcj1CNV2mK1C14A2mqoGYAAAAAxpSfaAecRf5cABYJ7L56ug==; "
                 "incap_ses_505_984766=x3VAGavj9hiKp59R8R4CB0TKoGYAAAAAG+aBVXOc2aIXQj3wKAKlXQ==; "
                 "AT=MTY4NTE1MTozOmE5dFdEZ1lGOGRh; DI=null; AI=null; U=583028766669e6026853a7d793f36; "
                 "laravel_token=eyJpdiI6IjgzakVSVEp4YmliZGdPanNNQmR4eFE9PSIsInZhbHVlIjoiUTliakRBQjVFY2RYczd1cldyV1hNNEFaejhZdkFqdWtsL3I5eWphZllQNSt1RThnWDRRd3VPbXpqT1VHRDVBOVhBU3hBMW1XOWtDYXowZEEzejh3MWtqcUtNNlVIS0tqdjloWTBGNUkyai9yajlLU1BMQnRWaFZKakhieUNHS0FXYXpUY2xUY05BbzYrWjBObnNkSFVPWUgwa01aUVdSZVI3aXlTTDk4QSthVWVYWmxDQ0JUVmRNR3dJRWdqc2pnYjkxWjh2YVNxa0lYSFQ4bmtRWkU3VzRTdHNVRWVvNDBkelQ1VG9RdWREalVYOVF2Q00vWFdDeFM5TWJ5anNHT01Udm5ZNFAzYitScy9PV0FScVBEcDY3YWkxMGdneXJVQWp2VGdXVUpvemgwcFRhQkFqUTRkQmJFOEc0YXRiTlAiLCJtYWMiOiI1Njc3NzY1MGMwZWJmMWIwZmI3OGVhYmM0NzIzZjIwM2I0ZDkyZDdlY2FiNDYwOWYyNWQ2YjI1NTM0MzMzZjBiIiwidGFnIjoiIn0%3D; "
                 "XSRF-TOKEN=eyJpdiI6IjFpOWNCQ2dWT1UrdjBtYjQwVVhFUVE9PSIsInZhbHVlIjoiWkpsNFcrYWdhTTBkd3FmLzZmOG9sZXF0eEdFQ1A5amRkVnNtZGRHUEd3Y2o2U1Z1am8wcVF2Lzc5L2dUODlrSTNyLzZGYjdKQm5VUGlNWUtVRmcyb0piT0M0OFNHc1BxKzVQU05mb0FLbSt4U0VZSVlOL2hla09TdVdIcUVmVU4iLCJtYWMiOiJiYTFjNmUxNjU0ZGQxOGM5YmJmOTVhYzdiNGEwZGU4ZGViYzY2YWFmM2Y1NjhhZGFlMmQ4Njg2M2M4MmJjYTBmIiwidGFnIjoiIn0%3D; "
                 "hemmings_session=eyJpdiI6InpDWnFyR0JYM01SMW8vY2w2MkFSUVE9PSIsInZhbHVlIjoiQk9lb2g0V0tVZ000MU9nVlhQaUtCbnVrSXhjYmxhK25oaEdQSHE4aWhPVW1YQStXKzVDS3VaM2Q3em56a3hYenBjTlQ1TlNXSXRuaWN4SG96QkRNTklQVXFKVFgxVnAreXNDR2h2RjNRTWhDaHM2b2grRmdSRkhDOWtuVnlxUWEiLCJtYWMiOiJmZTgwYTEwZDJlZDhlZDQyYzNlMjkyMDg5MWEyOGJjMTZkNTZlZmQ3ZmZkM2ZkYzNkMzQ5N2Y4MTAxMTBiOWE0IiwidGFnIjoiIn0%3D; "
                 "AWSALB=41fvJfgqCdoCv5Hds+jo/4IjObbrbFMVY6MUFEm4HXS3uHYkJoJU5Dg5ad38GyCemDa5O+rslfiHf+0YmouZaA1ncFFzL5MnTgaIR8ImaHPtq7aHkjSWK4D8ZVnShJJeu0fX/UNpYwp91442E2wgSVTBjAy6Aaq7U/RMH+fgL2mb/VX014V+YQVKFWa2paGsyuMAnx25qjexjLjTrx3zHK/SvUik8ST15sgG3V9HHPS8WtvwM8g9vAGvLZbUXck=; "
                 "AWSALBCORS=41fvJfgqCdoCv5Hds+jo/4IjObbrbFMVY6MUFEm4HXS3uHYkJoJU5Dg5ad38GyCemDa5O+rslfiHf+0YmouZaA1ncFFzL5MnTgaIR8ImaHPtq7aHkjSWK4D8ZVnShJJeu0fX/UNpYwp91442E2wgSVTBjAy6Aaq7U/RMH+fgL2mb/VX014V+YQVKFWa2paGsyuMAnx25qjexjLjTrx3zHK/SvUik8ST15sgG3V9HHPS8WtvwM8g9vAGvLZbUXck=")

# Set the headers, including the Cookie header
headers = {
    "Cookie": cookie_string,
    # Replace with an appropriate User-Agent string
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# Make the request to the specified URL
response = requests.get(
    "https://www.hemmings.com/stories-api/landing/featured-vehicles", headers=headers)

# Print the response status code and text
print(response.status_code)
print(response.text)
