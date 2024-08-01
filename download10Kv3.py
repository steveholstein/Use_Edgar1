'''
1. **Install Required Packages**:
```bash
pip install secedgar requests pandas beautifulsoup4 lxml
```

2. **Python Script**:
This script will automate the download and extraction of the relevant sections without needing manual adjustments.

```python
'''
import os
from secedgar import filings, FilingType
from bs4 import BeautifulSoup
from pathlib import Path

# Define the company CIK and the filing type
cik = '0000051143'  # IBM's CIK
f_type = FilingType.FILING_10K

# Define the destination directory
destination = './IBM_10K_filings'
Path(destination).mkdir(parents=True, exist_ok=True)

# Step 1: Download the most recent 10-K filing for IBM
ibm_filings = filings(cik_lookup=cik, filing_type=f_type, count=1, user_agent='greettingssteve@gmail.com')
ibm_filings.save(destination)

# Find the downloaded filing
filings_dir = os.path.join(destination, cik)
filing_file = None
for root, dirs, files in os.walk(filings_dir):
    for file in files:
        if file.endswith('.txt'):
            filing_file = os.path.join(root, file)
            break

if not filing_file:
    raise FileNotFoundError("10-K filing not found in the expected directory.")

# Step 2: Parse the filing to extract sections
with open(filing_file, 'r', encoding='utf-8') as f:
    content = f.read()

soup = BeautifulSoup(content, 'lxml')

# Function to find the text between two headings
def find_section(soup, start_text, end_text=None):
    start = soup.find(text=lambda t: t and start_text in t)
    if not start:
        return f"Section starting with '{start_text}' not found."
    section_content = []
    for elem in start.find_all_next():
        if end_text and elem.name in ["h1", "h2", "h3", "h4"] and end_text in elem.get_text():
            break
        section_content.append(elem.get_text(separator=' ', strip=True))
    return '\n'.join(section_content)

# Define sections and their respective headings
sections = {
    "Business Overview": "ITEM 1. BUSINESS",
    "Risk Factors": "ITEM 1A. RISK FACTORS",
    "Selected Financial Data": "ITEM 6. SELECTED FINANCIAL DATA",
    "MD&A": "ITEM 7. MANAGEMENT'S DISCUSSION AND ANALYSIS",
    "Financial Statements": "ITEM 8. FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA"
}

# Extract and save sections
for section_name, start_heading in sections.items():
    end_heading = None  # Assuming each section ends at the start of the next section or end of document
    if section_name != "Financial Statements":  # Financial Statements is usually the last section we care about
        next_section = list(sections.values())[list(sections.keys()).index(section_name) + 1]
        end_heading = next_section
    section_content = find_section(soup, start_heading, end_heading)
    section_file = os.path.join(destination, f"{section_name.replace(' ', '_')}.txt")
    with open(section_file, 'w', encoding='utf-8') as file:
        file.write(section_content)
    print(f"Extracted and saved {section_name}")

print("Extraction complete. Check the output files in the directory:", destination)
'''
```

### Explanation:

1. **Install Required Packages**:
   - Install the necessary packages with `pip install secedgar requests pandas beautifulsoup4 lxml`.

2. **Download the Filing**:
   - Use `secedgar` to download the most recent 10-K filing for IBM.
   - Save the filing in the specified directory.

3. **Find the Downloaded Filing**:
   - Search the directory for the downloaded filing.

4. **Parse the Filing**:
   - Use `BeautifulSoup` to parse the content of the 10-K filing.
   - Define a function `find_section` to extract text between two headings.

5. **Define Sections**:
   - Specify the section headings that you're interested in extracting.

6. **Extract and Save Sections**:
   - Iterate over the sections and use the `find_section` function to extract content.
   - Save each section's content to a separate text file.

### Summary:
This script automates the entire process of downloading and parsing IBM's 10-K filing for specific sections. It uses `BeautifulSoup` to locate the sections by their headings and extracts the text content between these headings. The sections are then saved into individual text files in the specified directory. This should work without needing manual adjustments for each filing.
'''
