import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def extract_contact_details(url):
    try:
        response = requests.get(url, timeout=30)  # Add timeout to handle hanging requests
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extracting contact details
        phone_number = soup.find('a', href=lambda href: href and 'tel:' in href)
        email = soup.find('a', href=lambda href: href and 'mailto:' in href)
        business_name = soup.find('meta', attrs={'property': 'og:site_name'})
        owner_name = soup.find('meta', attrs={'name': 'author'})
        business_address = soup.find('address')

        # Example of extracting elements based on class attributes
        phone_number_class = soup.find(class_='phone-class')
        email_class = soup.find(class_='email-class')
        business_name_class = soup.find(class_='business-name-class')
        owner_name_class = soup.find(class_='owner-name-class')
        business_address_class = soup.find(class_='business-address-class')

        # Safely access the 'content' attribute
        business_name_content = business_name['content'].strip() if business_name and 'content' in business_name.attrs else None
        owner_name_content = owner_name['content'].strip() if owner_name and 'content' in owner_name.attrs else None

        # Return a dictionary with extracted details
        return {
            'phone_number': phone_number.get_text(strip=True) if phone_number else (phone_number_class.get_text(strip=True) if phone_number_class else None),
            'email': email.get_text(strip=True) if email else (email_class.get_text(strip=True) if email_class else None),
            'business_name': business_name_content or (business_name_class.get_text(strip=True) if business_name_class else None),
            'owner_name': owner_name_content or (owner_name_class.get_text(strip=True) if owner_name_class else None),
            'business_address': business_address.get_text(strip=True) if business_address else (business_address_class.get_text(strip=True) if business_address_class else None),
            'error': None
        }
    except requests.exceptions.RequestException as e:
        # Log the request error and return None for contact details
        return {
            'phone_number': None, 
            'email': None, 
            'business_name': None, 
            'owner_name': None, 
            'business_address': None, 
            'error': str(e)
        }

# Attempt to read CSV file with error handling
try:
    # Read the CSV file with proper handling
    df = pd.read_csv('fileWithColumnCalledwebsite.csv', sep=',', quotechar='"')

    # Check for the 'website' column
    if 'website' not in df.columns:
        raise ValueError("Expected 'website' column not found in the CSV file.")
    
    # Clean the column names
    df.columns = df.columns.str.strip().str.replace('"', '')

except pd.errors.ParserError as e:
    print(f"Error reading CSV file: {e}")
    exit(1)
except ValueError as e:
    print(f"ValueError: {e}")
    exit(1)

# Create a log file with a timestamp
log_filename = datetime.now().strftime("scrape_log_%Y%m%d_%H%M%S.log")
output_filename = datetime.now().strftime("scraped_data_%Y%m%d_%H%M%S.csv")

# List to hold all extracted data for saving to a new CSV
extracted_data = []

with open(log_filename, 'w') as logfile:
    for index, row in df.iterrows():
        url = row['website']
        if pd.notna(url):
            contact_details = extract_contact_details(url)
            log_entry = f"Contact Details for {url}:\n"
            log_entry += f"Phone Number: {contact_details['phone_number']}\n"
            log_entry += f"Email: {contact_details['email']}\n"
            log_entry += f"Business Name: {contact_details['business_name']}\n"
            log_entry += f"Owner Name: {contact_details['owner_name']}\n"
            log_entry += f"Business Address: {contact_details['business_address']}\n"
            log_entry += f"Error (if any): {contact_details['error']}\n"
            log_entry += '--------------------------------------------------------------- \n \n \n'
            logfile.write(log_entry)
            print(log_entry)

            # Append the contact details to the list
            extracted_data.append({
                'website': url,
                'phone_number': contact_details['phone_number'],
                'email': contact_details['email'],
                'business_name': contact_details['business_name'],
                'owner_name': contact_details['owner_name'],
                'business_address': contact_details['business_address'],
                'error': contact_details['error']
            })

# Convert the list of dictionaries to a DataFrame and save it as a CSV
extracted_df = pd.DataFrame(extracted_data)
extracted_df.to_csv(output_filename, index=False)

print(f"Log file created: {log_filename}")
print(f"Extracted data saved to: {output_filename}")