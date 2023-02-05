#!/opt/homebrew/anaconda3/bin/python

import os
import sys
import json
import concurrent.futures
import requests

def download_file(item, save_path):
    # Get the file name from the URL
    url = item["url"]
    file_name = url.split("/")[-1]
    id = item["id"]
    extension = file_name.split(".")[-1]
    save_location = os.path.join(save_path, f"{id}.{extension}")

    # Check if the file is a png or jpg
    if extension not in ["png", "PNG", "jpg", "JPG", "jpeg", "JPEG"]:
        print(f"\nSkipping {id}.{extension}")
        return

    # Download the file
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get("Content-Length", 0))
    progress = 0
    with open(save_location, "wb") as f:
        for data in response.iter_content(1024):
            progress += len(data)
            f.write(data)
    print(f"\nDownloaded {id}.{extension}")


def main(json_file, save_path=None, max_workers=8):
    # Load the JSON file into memory
    with open(json_file) as file:
        data = json.load(file)

    # Set the default download path to be the name of the JSON file (minus the extension)
    if save_path is None:
        save_path = os.path.splitext(json_file)[0]

    # Create the download directory if it doesn't exist
    os.makedirs(save_path, exist_ok=True)

    # Download the files in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(download_file, item, save_path) for item in data]
        for future in concurrent.futures.as_completed(futures):
            future.result()

if __name__ == "__main__":
    # Check if the name of the JSON file was passed as an argument
    if len(sys.argv) < 2:
        print("Error: missing argument for JSON file name")
        sys.exit(1)

    # Get the name of the JSON file from the command-line arguments
    json_file = sys.argv[1]
    save_path = sys.argv[2] if len(sys.argv) >= 3 else None
    max_workers = int(sys.argv[3]) if len(sys.argv) >= 4 else 8

    # Call the main function
    main(json_file, save_path, max_workers)
