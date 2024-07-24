
import logging
import json
import configparser
import requests
from pathlib import Path
from extract_data import get_data
# from get_cookies import get_cookies

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='[ %(levelname)s ] -- %(message)s')
logger = logging.getLogger(__name__)
config = configparser.ConfigParser()
config.read("config.ini")

# cookies = get_cookies()


def transform_url(url):
    base_url = 'https://www.hemmings.com'
    auction_id = url.split('/')[-1]
    return f'{base_url}/v2/auctions/listing/{auction_id}/gallery-images'


def fetch_gallery_data(url):
    headers = {key: config["LISTING_HEADERS"].get(
        key, '') for key in config["LISTING_HEADERS"]}
    headers["Cookie"] = ("OptanonConsent=groups%3DC0004%3A0; visid_incap_2011533=/oIGRmwESOOOCHCTcLiH++BVnmYAAAAAQkIPAAAAAAC8jmZkX2dOepDP9CkIjeRE; "
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

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {}


def add_data_to_file(file_path):
    # Read the JSON data
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Iterate over each item in the 'results' key list
    logging.info(f"Processing {len(data.get('results', []))} items")
    for item in data.get('results', []):
        logging.info(f"Processing item: {item.get('id')}")
        if item.get('type') == 'auction':
            # Transform the URL and fetch gallery data
            url = item.get('url')
            if url:
                new_url = transform_url(url)
                gallery_data = fetch_gallery_data(new_url)
                other_data = get_data(
                    url, '//*[@id = "app"]/div[2]/div/div/div[3]/div[1]/div/div[2]/div/div[2]')

                # Add the gallery data to the current item
                item['gallery'] = gallery_data
                item['other_data'] = other_data
            else:
                logger.error("URL not found in item")

                # Save the modified data back to the file
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)
    return Path('data.json').resolve()


def fetch_hemings_data():
    """
    Fetches data from the Hemmings API using parameters from the configuration file.
    Writes the response to 'response.json' and returns the absolute path to the file.

    Returns:
        Path: Absolute path to the saved response file, or None if an error occurs.
    """

    url = config["API"]["url"]
    params = {key: config["PARAMS"].get(key, '') for key in config["PARAMS"]}
    headers = {key: config["HEADERS"].get(
        key, '') for key in config["HEADERS"]}
    # params["per_page"] = str(int(params.get('page', '1')) * 30)
    params["per_page"] = '1'
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Request failed: {e}")
        return None

    response_path = Path("response.json")
    try:
        response_path.write_text(response.text)
    except IOError as e:
        logger.error(f"Failed to write to file: {e}")
        return None

    return response_path.resolve()


def upload_file(file_path):
    """
    Uploads the specified file to the Gofile API and returns the download URL.

    Args:
        file_path(Path): The path to the file to be uploaded.

    Returns:
        str: The download URL of the uploaded file.

    Raises:
        ValueError: If the download URL is not found in the response.
    """
    try:
        servers = requests.get('https://api.gofile.io/servers').json()
        server = servers["data"]["servers"][0]["name"]
    except (requests.RequestException, KeyError) as e:
        logger.error(f"Failed to get server information: {e}")
        return None

    gofile_url = f"https://{server}.gofile.io/uploadFile"
    try:
        with open(file_path, 'rb') as file:
            response = requests.post(gofile_url, files={'file': file})
            response.raise_for_status()
            result = response.json()
    except (requests.RequestException, IOError) as e:
        logger.error(f"Failed to upload file: {e}")
        return None

    download_url = result.get('data', {}).get('downloadPage')
    if download_url:
        return download_url
    else:
        raise ValueError("Failed to get download URL")


if __name__ == "__main__":
    try:
        file = fetch_hemings_data()
        if file:
            file_path = add_data_to_file(file)
            url = upload_file(file_path)
            if url:
                logger.info(f"Download URL: {url}")
    except Exception as e:
        logger.exception(f"Error: {e}")
