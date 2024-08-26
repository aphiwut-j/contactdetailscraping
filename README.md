# contactdetailscraping
This is my experiment about web scraping. It aim to only gather contact detail from websites, but still need more enhancement because it couldn't gather from all the web structures.



# Project Overview
This project is a Python script designed to extract contact details (such as phone numbers, emails, business names, owner names, and addresses) from a list of websites. The script reads a CSV file containing URLs, scrapes each site for relevant information, and then logs the results into a new CSV file and a log file.

# Prerequisites
Before running the script, make sure you have the following installed:

- Python 3.x
- Pandas library
- Requests library
- BeautifulSoup4 (from the bs4 package)
You can install the required Python packages using pip: 'pip install pandas requests beautifulsoup4'

# How the Script Works
1. Read the Input CSV File:
- The script reads a CSV file named 1000lines.csv. This file should contain a column named website, which lists the URLs to be scraped.

2. Extract Contact Details:
- For each URL, the script sends a GET request to the website and parses the HTML content using BeautifulSoup.
- It attempts to extract the following information:
 - Phone Number
 - Email Address
 - Business Name
 - Owner Name
 - Business Address
- If the contact details are not found using direct HTML tags, the script looks for them using specific class attributes (e.g., 'phone-class', 'email-class').

3. Handle Errors:
- The script includes error handling for request timeouts and other exceptions. If a website cannot be accessed or data cannot be extracted, the error is logged, and the script moves on to the next URL.

4. Logging and Output:
- The script generates a log file and a CSV file. The log file contains detailed information about the scraping process for each URL, and the CSV file stores the extracted contact details.
- Filenames are generated based on the current timestamp to ensure they are unique.

# File Descriptions
- fileWithColumnCalledwebsite.csv: The input CSV file containing a column named website with URLs to be scraped.
- scrape_log_YYYYMMDD_HHMMSS.log: The log file created by the script, where YYYYMMDD_HHMMSS is the timestamp of when the script was run.
- scraped_data_YYYYMMDD_HHMMSS.csv: The output CSV file with the extracted contact details.
  
# Usage Instructions

1. Prepare the CSV file:
- Ensure that 1000lines.csv is in the same directory as the script and contains a website column with URLs.

2. Run the Script:
- Execute the script using Python: 'python script_name.py'
- Replace script_name.py with the actual name of your script file.

3. Check the Outputs:
- After the script completes, check the directory for the log file and the CSV file with the extracted data.
  
# Error Handling
- The script includes error handling for common issues such as network errors or missing data in the HTML. Any errors encountered during scraping are logged in the log file.

# Modifying the Script
- Changing the CSV File: If your input CSV file has a different name or structure, modify the pd.read_csv('1000lines.csv') line accordingly.
- Customizing HTML Tags or Classes: If you need to scrape different tags or classes, update the relevant sections in the extract_contact_details() function.

# License
This project is provided "as is" without warranty of any kind, express or implied. Feel free to modify and use the code for your own purposes.
