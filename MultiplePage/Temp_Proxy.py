from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv
import json
import pandas as pd
import random

# List of proxies
proxies = [
    "198.49.68.8",
    "35.185.196.38",
    "45.77.98.113",
    "35.185.196.38",
    "64.23.223.154"
]

def get_random_proxy():
    return random.choice(proxies)

# Function to initialize the Chrome driver with a proxy
def init_driver(proxy=None):
    chrome_options = Options()
    if proxy:
        chrome_options.add_argument(f'--proxy-server={proxy}')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

# Initialize the Chrome driver with a random proxy
proxy = get_random_proxy()
driver = init_driver(proxy)

query = "it-jobs"
base_url = f"https://www.naukri.com/{query}?src=gnbjobs_homepage_srch"
driver.get(base_url)

# Lists to store data
all_data = []

page = 1
while True:
    time.sleep(5)  # Wait for the page to load

    # Get the page source and parse it with BeautifulSoup
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Your existing code to extract data goes here...

    # Rotate the proxy after a few pages or if blocked
    if page % 3 == 0:  # Change proxy every 3 pages
        print("Changing proxy...")
        driver.quit()
        proxy = get_random_proxy()
        driver = init_driver(proxy)
        driver.get(base_url)  # Navigate to the page again

    print(f"Page {page} data collected")

    # Find and click the "Next" link
    try:
        pagination_div = driver.find_element(By.CSS_SELECTOR, "div.styles_pagination__oIvXh")
        next_links = pagination_div.find_elements(By.CSS_SELECTOR, "a.styles_btn-secondary__2AsIP")

        if len(next_links) > 1:
            next_link = next_links[1]
            if next_link.is_displayed() and next_link.is_enabled():
                driver.execute_script("arguments[0].click();", next_link)
                page += 1
                time.sleep(3)
                if page == 5:
                    break
            else:
                print("No 'Next' link found or link not clickable. Ending pagination.")
                break
        else:
            print("No 'Next' link found. Ending pagination.")
            break
    except Exception as e:
        print(f"Error during pagination: {e}")
        break

# Close the driver
driver.quit()

# Save data to CSV
csv_file = "job_data2.csv"
keys = all_data[0].keys()
with open(csv_file, "w", newline="", encoding="utf-8") as output_file:
    dict_writer = csv.DictWriter(output_file, fieldnames=keys)
    dict_writer.writeheader()
    dict_writer.writerows(all_data)

# Save data to Excel
excel_file = "job_data2.xlsx"
df = pd.DataFrame(all_data)
df.to_excel(excel_file, index=False)

# Save data to JSON
json_file = "job_data2.json"
with open(json_file, "w", encoding="utf-8") as json_output_file:
    json.dump(all_data, json_output_file, ensure_ascii=False, indent=4)

print("Data saved to CSV, Excel, and JSON files.")
