import logging
import json
import configparser
import requests
from pathlib import Path
from extract_data import get_data

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='[ %(levelname)s ] -- %(message)s')
logger = logging.getLogger(__name__)
config = configparser.ConfigParser()
config.read("config.ini")


def transform_url(url):
    base_url = 'https://www.hemmings.com'
    auction_id = url.split('/')[-1]
    return f'{base_url}/v2/auctions/listing/{auction_id}/gallery-images'


def fetch_gallery_data(url):
    headers = {key: config["LISTING_HEADERS"].get(
        key, '') for key in config["LISTING_HEADERS"]}
    with open('cookie.txt', 'r') as file:
        cookie = file.read().strip()
    headers["Cookie"] = cookie
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
