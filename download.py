#!/opt/homebrew/anaconda3/bin/python

import os
import sys
import json
import concurrent.futures
import requests

def download_file(url, save_path):
    # Get the file name from the URL
    file_name = url.split("/")[-1]
    save_location = os.path.join(save_path, file_name)

    # Download the file
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get("Content-Length", 0))
    progress = 0
    with open(save_location, "wb") as f:
        for data in response.iter_content(1024):
            progress += len(data)
            f.write(data)
            done = int(50 * progress / total_size)
            print(f"{file_name}: [{'=' * done}>{' ' * (50-done)}] {progress}/{total_size}", end="")
    print(f"\nDownloaded {file_name}")

def main(json_file, save_path, max_workers):
    # Load the JSON file into memory
    with open(json_file) as file:
        data = json.load(file)

    # Extract the URLs from the JSON data
    urls = [item["url"] for item in data]

    # Create the download directory if it doesn't exist
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # Download the files in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(download_file, url, save_path) for url in urls]
        for future in concurrent.futures.as_completed(futures):
            future.result()

if __name__ == "__main__":
    # Check if the name of the JSON file and the download location were passed as arguments
    if len(sys.argv) < 2:
        print("Error: missing argument for JSON file name")
        sys.exit(1)

    # Get the name of the JSON file from the command-line arguments
    json_file = sys.argv[1]
    
    # Set the download location to the same name as the json file, but without the extension
    save_path = os.path.splitext(json_file)[0]
    if len(sys.argv) >= 3:
        save_path = sys.argv[2]
    
    # Set the number of concurrent downloads
    max_workers = 8
    if len(sys.argv) >= 4:
        max_workers = int(sys.argv[3])

    # Call the main function
    main(json_file, save_path, max_workers)
