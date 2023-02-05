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
            print(f"\r[{'=' * done}>{' ' * (50-done)}] {progress}/{total_size}", end="")
    print(f"\nDownloaded {file_name}")

def main(json_file, save_path):
    # Load the JSON file into memory
    with open(json_file) as file:
        data = json.load(file)

    # Extract the URLs from the JSON data
    urls = [item["url"] for item in data]

    # Download the files in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(download_file, url, save_path) for url in urls]
        for future in concurrent.futures.as_completed(futures):
            future.result()

if __name__ == "__main__":
    # Check if the name of the JSON file and the download location were passed as arguments
    if len(sys.argv) < 3:
        print("Error: missing arguments for JSON file name and download location")
        sys.exit(1)

    # Get the name of the JSON file and the download location from the command-line arguments
    json_file = sys.argv[1]
    save_path = sys.argv[2]

    # Call the main function
    main(json_file, save_path)
