# pip install sec-edgar-downloader

from sec_edgar_downloader import Downloader
from pathlib import Path
import os

# You can replace '.' with a specific directory path if desired
destination = r'C:\Users\hello\PycharmProjects\Use_Edgar1\APPLE_10K_filings'

# Ensure the destination directory exists
Path(destination).mkdir(parents=True, exist_ok=True)

absolute_path = os.path.abspath(destination)
print("Absolute path:", absolute_path)


# Initialize a downloader instance with a specific download directory
dl = Downloader("Ed22", "greetingssteve@gmail.com", download_folder=destination)

# Download all 10-K filings for a specific company (e.g., Apple)
dl.get("10-K", "AAPL")

'''
#List Files in the Directory: After the download, list the files in the directory to confirm they are there:
files = os.listdir(destination)
print("Files in directory:", files)

#Check for Subdirectories: The sec-edgar-downloader package might create subdirectories based on the company ticker and filing type.
for root, dirs, files in os.walk(destination):
    for name in files:
        print(os.path.join(root, name))

'''
