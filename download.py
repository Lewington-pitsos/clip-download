#!/opt/homebrew/anaconda3/bin/python

import os
import sys
import json
import concurrent.futures
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def download_file(item, save_path):
    # Get the file name from the URL
    url = item["url"]
    file_name = url.split("/")[-1]
    id = item["id"]
    extension = file_name.split(".")[-1]
    save_location = os.path.join(save_path, f"{id}.{extension}")

    # Check if the file is a png or jpg
    if extension not in ["png", "jpg", "jpeg"]:
        print(f"\nSkipping {id}.{extension}")
        return

    # Download the file
    session = requests.Session()
    retry = Retry(total=5, backoff_factor=0.1, status_forcelist=[ 500, 502, 503, 504 ])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    response = session.get(url, stream=True)
    total_size = int(response.headers.get("Content-Length", 0))
    progress = 0
    with open(save_location, "wb") as f:
        for data in response.iter_content(1024):
            progress += len(data)
            f.write(data)
    print(f"\nDownloaded {id}.{extension}")


def main(json_file, save_path, max_workers):
    # Load the JSON file into memory
    with open(json_file) as file:
        data = json.load(file)

    # Create the download directory if it doesn't exist
    os.makedirs(save_path, exist_ok=True)

    # Download the files in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(download_file, item, save_path) for item in data]
        for future in concurrent.futures.as_completed(futures):
            future.result()

if __name__ == "__main__":
    # Check if the name of the JSON file and the download location were passed as arguments
    if len(sys.argv) < 2:
        print("Error: missing argument for JSON file name")
        sys.exit(1)
    elif len(sys.argv) < 3:
        print("Error: missing argument for download location")
        sys.exit(1)

    # Get the name of the JSON file and the download location from the command-line arguments
    json_file = sys.argv[1]
    save_path = os.path.splitext(json_file)[0] if len(sys.argv) < 3 else sys.argv[2]
    max_workers = 8 if len(sys.argv) < 4 else int(sys.
