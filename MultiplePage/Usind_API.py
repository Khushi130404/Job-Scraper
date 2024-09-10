import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import json

# ScraperAPI key
SCRAPERAPI_API_KEY = "5e1a841368df1bf578442967a1c3595d"


# Function to get content using ScraperAPI
def fetch_content(url):
    try:
        response = requests.get('https://api.scraperapi.com/', params={
            'api_key': SCRAPERAPI_API_KEY,
            'url': url
        })
        print(f"Response Status Code: {response.status_code}")  # Print status code
        print(f"Response Content (first 1000 chars): {response.text[:1000]}")  # Print first 1000 characters of response

        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}. Response content: {response.text}")

        response.raise_for_status()  # Ensure we notice bad responses
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return ""


# URL to scrape
query = "it-jobs"
base_url = f"https://www.naukri.com/{query}?src=gnbjobs_homepage_srch"

# Fetch content using ScraperAPI
page_content = fetch_content(base_url)
soup = BeautifulSoup(page_content, 'html.parser')

# Example: Extract job titles and links
job_elements = soup.find_all('a', class_='title')  # Adjust the class name as needed
all_data = []

for job_element in job_elements:
    job_data = {
        'title': job_element.get_text(strip=True),
        'link': job_element.get('href', 'No link available')  # Use .get() to handle missing 'href'
    }
    all_data.append(job_data)

if all_data:
    # Save data to CSV
    csv_file = "job_data3.csv"
    keys = all_data[0].keys()
    with open(csv_file, "w", newline="", encoding="utf-8") as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(all_data)

    # Save data to Excel
    excel_file = "job_data3.xlsx"
    df = pd.DataFrame(all_data)
    df.to_excel(excel_file, index=False)

    # Save data to JSON
    json_file = "job_data3.json"
    with open(json_file, "w", encoding="utf-8") as json_output_file:
        json.dump(all_data, json_output_file, ensure_ascii=False, indent=4)

    print("Data saved to CSV, Excel, and JSON files.")
else:
    print("No data was collected.")
