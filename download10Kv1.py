
import edgar
import requests
import pandas as pd
from pathlib import Path
# Define the year and destination directory
year = '2023'
destination = '.'
# Ensure the destination directory exists
Path(destination).mkdir(parents=True, exist_ok=True)
# Step 1: Download the index files for the specified year
edgar.download_index(year, destination=destination)
print(f"Index files for the year {year} have been downloaded to {destination}.")
# Step 2: Use the `edgar` package to fetch IBM's 10-K filings
# Define the company
company = edgar.Company("IBM", "0000051143")
# Get all filings of type 10-K
tree = company.get_all_filings(filing_type="10-K")
# Convert filings tree to DataFrame
filings_list = []
for result in tree.getchildren():
    for filing in result.getchildren():filing_info = {}
    for child in filing.getchildren():tag = child.tag.split('}')[1]
filing_info[tag] = child.text
filings_list.append(filing_info)
filings_df = pd.DataFrame(filings_list)
# Path to save the DataFrame as Excel
excel_path = f"{destination}/IBM_10K_filings.xlsx"
# Save the filings DataFrame to an Excel file
filings_df.to_excel(excel_path, index=False)
print(f"IBM's 10-K filings have been saved to {excel_path}.")
# Step 3: Read and save the most recent 10-K filing
# Get the URL of the most recent 10-K filing
recent_10k_url = filings_df.iloc[0]['url']
# Fetch the content of the most recent 10-K filing
response = requests.get(recent_10k_url)
# Path to save the content of the most recent 10-K filing
content_path = f"{destination}/IBM_10-K.txt"
with open(content_path, 'w') as file:
    file.write(response.text)
print(f"The most recent IBM 10-K filing has been saved to {content_path}.")
